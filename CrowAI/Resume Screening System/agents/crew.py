"""
agents/crew.py — BatchScreeningCrew (with CHUNKED batching)

Processes resumes in SMALL BATCHES rather than one giant prompt or one-by-one:
  Parser → Matcher → Advisor   (per chunk, repeated for each chunk)
  Email Drafter                (also chunked, runs on the merged results)

━━━ WHY CHUNKING? ━━━
  ❌ One giant batch (e.g. 15 resumes in a single prompt):
     - Risks exceeding the model's context window
     - Output gets truncated mid-JSON → broken parsing
     - The LLM can mix up details between candidates (hallucination/cross-talk)

  ❌ One-by-one (1 resume per call):
     - Accurate, but slow (N x round trips)
     - No consistent rubric — candidate #1 may be scored more leniently than #10

  ✅ Chunked batching (default: 4 candidates per call):
     - Small enough to stay inside context limits reliably
     - Large enough that agents still compare candidates within a chunk
       for relative, consistent scoring
     - Total LLM calls ≈ ceil(N / chunk_size) × 3, not N × 3

Outputs are saved per-agent (merged across all chunks) to results/outputs/:
  parse_output.json
  match_output.json
  advisor_output.json
  email_output.json

Per-chunk raw outputs are also saved (chunk_1_parse.json, chunk_2_match.json, ...)
so you can inspect exactly what each batch produced.
"""

import json
import re
from pathlib import Path

from crewai import Crew, Process

from .parser      import create_parser_agent,  create_parse_task
from .matcher     import create_matcher_agent,  create_match_task
from .advisor     import create_advisor_agent,  create_advise_task
from .email_agent import create_email_agent,    create_email_task

# Tune based on your model's context window and average resume length.
# Smaller = safer/more accurate, larger = fewer LLM calls but more truncation risk.
DEFAULT_CHUNK_SIZE = 4


class BatchScreeningCrew:
    """
    One crew instance, candidates processed in chunked batches.
    Call .screen() with a dict of {candidate_name: resume_text}.
    """

    def __init__(
        self,
        llm,
        job_description: str,
        position: str,
        company: str,
        interview_slots: str = "Monday–Thursday, 10 AM – 4 PM",
        output_dir: Path | None = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ):
        self.llm             = llm
        self.job_description = job_description
        self.position        = position
        self.company         = company
        self.interview_slots = interview_slots
        self.output_dir      = Path(output_dir) if output_dir else None
        self.chunk_size      = max(1, chunk_size)

        # Agents — created once, reused across all chunks
        self.parser_agent  = create_parser_agent(llm)
        self.matcher_agent = create_matcher_agent(llm)
        self.advisor_agent = create_advisor_agent(llm)
        self.email_agent   = create_email_agent(llm)

    # ── Public API ────────────────────────────────────────────────────────────

    def screen(self, resumes: dict[str, str]) -> tuple[list[dict], list[dict]]:
        """
        Screen all resumes, processed in chunks of self.chunk_size candidates.

        Args:
            resumes: {candidate_name: resume_text}

        Returns:
            (advisor_results, email_drafts) — both list[dict], all candidates merged
        """
        all_names = list(resumes.keys())
        chunks    = self._make_chunks(all_names, self.chunk_size)
        n_chunks  = len(chunks)

        all_parse  : list[dict] = []
        all_match  : list[dict] = []
        all_advise : list[dict] = []

        print(f"\n📦  Splitting {len(all_names)} candidate(s) into {n_chunks} "
              f"batch(es) of up to {self.chunk_size} each (avoids context overflow "
              f"and cross-candidate hallucination).")

        for idx, name_chunk in enumerate(chunks, 1):
            chunk_resumes = {n: resumes[n] for n in name_chunk}
            print(f"\n{'─'*54}")
            print(f"⚙️   Batch {idx}/{n_chunks}: {', '.join(name_chunk)}")
            print(f"{'─'*54}")

            parse_data, match_data, advise_data = self._run_chunk(chunk_resumes, name_chunk)

            all_parse.extend(parse_data)
            all_match.extend(match_data)
            all_advise.extend(advise_data)

            if self.output_dir:
                self.output_dir.mkdir(parents=True, exist_ok=True)
                self._save(parse_data,  f"chunk_{idx}_parse.json")
                self._save(match_data,  f"chunk_{idx}_match.json")
                self._save(advise_data, f"chunk_{idx}_advisor.json")

        # ── Post-process: attach email + flags to advisor results ──────────────
        for i, adv in enumerate(all_advise):
            # Guard: a malformed batch can yield a non-dict (e.g. a bare string)
            # in the results list. Coerce it to a safe empty advisor record so
            # the run never crashes on `'str' object has no attribute setdefault`.
            if not isinstance(adv, dict):
                name = f"Candidate {i + 1}"
                if i < len(all_parse) and isinstance(all_parse[i], dict):
                    name = all_parse[i].get("full_name") or name
                adv = self._empty_advise(name)
                all_advise[i] = adv

            parse_i = all_parse[i] if (i < len(all_parse) and isinstance(all_parse[i], dict)) else {}
            adv.setdefault("email", parse_i.get("email", ""))
            adv.setdefault("position_applied", self.position)
            adv.setdefault("qualified", adv.get("total_score", 0) >= 60)
            adv.setdefault("accepted",  adv.get("recommendation") == "Advance to Interview")

        # ── Email drafting — also chunked, run on the merged advisor results ───
        all_email = self._draft_emails_chunked(all_advise)

        # ── Save merged outputs ─────────────────────────────────────────────────
        if self.output_dir:
            self._save(all_parse,  "parse_output.json")
            self._save(all_match,  "match_output.json")
            self._save(all_advise, "advisor_output.json")
            self._save(all_email,  "email_output.json")
            print(f"\n💾  Merged agent outputs saved to: {self.output_dir}")

        return all_advise, all_email

    # ── Per-chunk pipeline ────────────────────────────────────────────────────

    def _run_chunk(
        self,
        chunk_resumes: dict[str, str],
        name_chunk: list[str],
    ) -> tuple[list[dict], list[dict], list[dict]]:
        """Run Parser → Matcher → Advisor on one small batch of candidates."""

        parse_task  = create_parse_task(self.parser_agent, chunk_resumes)
        match_task  = create_match_task(self.matcher_agent, self.job_description, parse_task)
        advise_task = create_advise_task(self.advisor_agent, name_chunk, parse_task, match_task)

        crew = Crew(
            agents=[self.parser_agent, self.matcher_agent, self.advisor_agent],
            tasks=[parse_task, match_task, advise_task],
            process=Process.sequential,
            verbose=True,
        )
        crew.kickoff()

        parse_raw  = getattr(parse_task.output,  "raw", "")
        match_raw  = getattr(match_task.output,  "raw", "")
        advise_raw = getattr(advise_task.output, "raw", "")

        parse_data  = self._parse_json_array(parse_raw,  name_chunk, self._empty_parse)
        match_data  = self._parse_json_array(match_raw,  name_chunk, self._empty_match)
        advise_data = self._parse_json_array(advise_raw, name_chunk, self._empty_advise)

        # ── Per-chunk integrity check ───────────────────────────────────────
        # If a chunk returns the wrong item count, the LLM likely merged or
        # dropped a candidate — flag it and realign by index instead of
        # silently shipping misaligned data.
        for label, data in [("parse", parse_data), ("match", match_data), ("advise", advise_data)]:
            if len(data) != len(name_chunk):
                print(f"    ⚠️  {label} output count ({len(data)}) != batch size "
                      f"({len(name_chunk)}) — realigning by index.")
                data[:] = self._align_to_count(data, name_chunk)

        return parse_data, match_data, advise_data

    @staticmethod
    def _align_to_count(data: list[dict], names: list[str]) -> list[dict]:
        """Force a result list to match the expected candidate count, preserving order."""
        target = len(names)
        if len(data) > target:
            return data[:target]
        while len(data) < target:
            data.append({"candidate_name": names[len(data)], "_alignment_warning": True})
        return data

    # ── Email drafting (also chunked) ────────────────────────────────────────

    def _draft_emails_chunked(self, advise_data: list[dict]) -> list[dict]:
        chunks    = self._make_chunks(advise_data, self.chunk_size)
        all_email: list[dict] = []

        print(f"\n✉️   Drafting emails in {len(chunks)} batch(es)…")

        for idx, candidate_chunk in enumerate(chunks, 1):
            email_task = create_email_task(
                self.email_agent,
                candidate_chunk,
                self.position,
                self.company,
                self.interview_slots,
            )
            email_crew = Crew(
                agents=[self.email_agent],
                tasks=[email_task],
                process=Process.sequential,
                verbose=False,
            )
            email_crew.kickoff()
            raw   = getattr(email_task.output, "raw", "[]")
            names = [c.get("candidate_name", "") for c in candidate_chunk]
            data  = self._parse_json_array(raw, names, self._empty_email)

            if len(data) != len(candidate_chunk):
                print(f"    ⚠️  email batch {idx} count mismatch — realigning by index.")
                data = self._align_to_count(data, names)

            all_email.extend(data)

            if self.output_dir:
                self._save(data, f"chunk_{idx}_email.json")

        return all_email

    # ── Chunking helper ───────────────────────────────────────────────────────

    @staticmethod
    def _make_chunks(items: list, size: int) -> list[list]:
        return [items[i:i + size] for i in range(0, len(items), size)]

    # ── Save / parse helpers ──────────────────────────────────────────────────

    def _save(self, data: list[dict], filename: str):
        path = self.output_dir / filename
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    @staticmethod
    def _parse_json_array(raw: str, names: list[str], empty_fn) -> list[dict]:
        """Extract a JSON array from raw LLM output; fallback to empty objects."""
        clean = re.sub(r"```(?:json)?\s*", "", raw or "").replace("```", "").strip()

        def _valid(d) -> bool:
            # Only accept a non-empty list whose items are ALL dicts. A list of
            # strings (or an inner array like ["Python","PyTorch"] accidentally
            # captured by the regex) must NOT be treated as candidate records.
            return isinstance(d, list) and len(d) > 0 and all(isinstance(x, dict) for x in d)

        try:
            data = json.loads(clean)
            if _valid(data):
                return data
        except json.JSONDecodeError:
            pass

        # Greedy match grabs the OUTERMOST array. A non-greedy match (\[[\s\S]*?\])
        # would stop at the first inner "]" of a nested list and return garbage.
        matches = re.findall(r"\[[\s\S]*\]", clean)
        for block in sorted(matches, key=len, reverse=True):
            try:
                data = json.loads(block)
                if _valid(data):
                    return data
            except json.JSONDecodeError:
                continue

        print(f"    ⚠️  Could not parse JSON array from output — using fallback for this batch.")
        return [empty_fn(n) for n in names]

    @staticmethod
    def _empty_parse(name: str) -> dict:
        return {
            "full_name": name, "email": "", "contact_info": "",
            "education": [], "years_of_experience": 0.0,
            "technical_skills": [], "work_experience": [],
            "notable_projects": [], "certifications_publications": [],
            "red_flags": ["Parse error — manual review required"],
        }

    @staticmethod
    def _empty_match(name: str) -> dict:
        return {
            "score_breakdown": {
                "technical_skills": 0, "experience_level": 0,
                "education_credentials": 0, "projects_portfolio": 0,
            },
            "total_score": 0,
            "strengths": [], "gaps": ["Could not evaluate — parse error"],
            "fit_verdict": "Poor Fit",
        }

    @staticmethod
    def _empty_advise(name: str) -> dict:
        return {
            "candidate_name": name, "email": "",
            "total_score": 0,
            "score_breakdown": {
                "technical_skills": 0, "experience_level": 0,
                "education_credentials": 0, "projects_portfolio": 0,
            },
            "fit_verdict": "Poor Fit",
            "strengths": [], "gaps": ["Error — manual review required"],
            "recommendation": "Manual Review Required",
            "suggested_interview_questions": [],
            "hiring_notes": "Error during processing. Please review manually.",
        }

    @staticmethod
    def _empty_email(name: str) -> dict:
        return {"to": "", "subject": "", "body": "", "email_type": "rejection"}
