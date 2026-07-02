"""
main.py — CLI entry point for the Resume Screening System.

Usage:
    python main.py
    python main.py --job path/to/job.txt --resumes path/to/resumes/
    python main.py --job job.txt --resumes cv1.pdf,cv2.pdf,cv3.docx
    python main.py --chunk-size 3      # smaller batches — safer for small-context models
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

from llm_loader    import get_llm_from_env
from resume_loader import load_all_resumes
from agents        import BatchScreeningCrew, save_html_report

load_dotenv()


def parse_args():
    p = argparse.ArgumentParser(description="Resume Screening System — CrewAI")
    p.add_argument("--job",     default=None, help="Path to job description file")
    p.add_argument("--resumes", default=None, help="Comma-separated paths to resume files/dirs")
    p.add_argument("--output",  default=None, help="Output directory (overrides .env)")
    p.add_argument("--company", default=None, help="Company name (overrides .env)")
    p.add_argument("--slots",   default=None, help="Interview availability string")
    p.add_argument("--chunk-size", type=int, default=None,
                    help="Candidates per LLM batch call (default: from .env CHUNK_SIZE or 4). "
                         "Lower = safer against context overflow / hallucination on large "
                         "resume sets or small-context local models.")
    return p.parse_args()


def main():
    print("\n" + "═" * 62)
    print("  🧑‍💼  Resume Screening System — powered by Crew AI")
    args = parse_args()

    print("\n" + "═" * 62)
    print("  🧑‍💼  Resume Screening System — powered by CrewAI")
    print("═" * 62 + "\n")

    base_dir    = Path(__file__).parent
    results_dir = Path(args.output or os.getenv("RESULTS_DIR", "results/"))
    output_dir  = results_dir / "outputs"
    results_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True,  exist_ok=True)

    # ── Job description ───────────────────────────────────────────────────────
    job_path = Path(args.job) if args.job else base_dir / os.getenv("JOB_DESCRIPTION_FILE", "job_description.txt")
    if not job_path.exists():
        print(f"❌  Job description not found: {job_path}")
        sys.exit(1)

    job_description = job_path.read_text(encoding="utf-8")
    position = "Open Position"
    company  = args.company or os.getenv("COMPANY_NAME", "Our Company")
    for line in job_description.splitlines():
        if line.lower().startswith("position:"):
            position = line.split(":", 1)[1].strip()
            break

    print(f"📄  Job     : {position} @ {company}")

    # ── Resumes ───────────────────────────────────────────────────────────────
    raw_paths = args.resumes or os.getenv("RESUMES_PATHS") or os.getenv("RESUMES_DIR", "resumes/")
    sources   = [base_dir / p.strip() for p in raw_paths.split(",") if p.strip()]
    resumes   = load_all_resumes(sources)

    if not resumes:
        print("❌  No resumes found. Check your paths.")
        sys.exit(1)

    print(f"📁  Resumes : {len(resumes)} found — {', '.join(resumes.keys())}")

    # ── LLM ───────────────────────────────────────────────────────────────────
    try:
        llm = get_llm_from_env()
        print(f"🤖  LLM     : {os.getenv('OLLAMA_MODEL') or os.getenv('OPENAI_MODEL')} "
              f"via {os.getenv('LLM_PROVIDER')}")
    except Exception as e:
        print(f"❌  LLM init failed: {e}")
        sys.exit(1)

    # ── Settings ───────────────────────────────────────────────────────────────
    chunk_size = args.chunk_size or int(os.getenv("CHUNK_SIZE", 4))
    threshold  = int(os.getenv("MIN_SCORE_THRESHOLD", 60))
    slots      = args.slots or os.getenv("INTERVIEW_SLOTS", "Monday–Thursday, 10 AM – 4 PM")

    n_batches = -(-len(resumes) // chunk_size)  # ceil division
    print(f"📦  Batching : {chunk_size} candidate(s)/call → {n_batches} batch(es) total")
    print(f"🎯  Threshold: {threshold}/100\n")

    # ── Run ────────────────────────────────────────────────────────────────────
    crew = BatchScreeningCrew(
        llm             = llm,
        job_description = job_description,
        position        = position,
        company         = company,
        interview_slots = slots,
        output_dir      = output_dir,
        chunk_size      = chunk_size,
    )

    advisor_results, email_drafts = crew.screen(resumes)

    # ── Save full JSON ────────────────────────────────────────────────────────
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    json_path = results_dir / f"results_{stamp}.json"
    json_path.write_text(
        json.dumps(
            {"position": position, "company": company,
             "candidates": advisor_results, "emails": email_drafts},
            indent=2, ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    # ── HTML report ───────────────────────────────────────────────────────────
    html_path = save_html_report(
        candidates   = advisor_results,
        email_drafts = email_drafts,
        position     = position,
        company      = company,
        results_dir  = results_dir,
        threshold    = threshold,
    )

    # ── Summary ───────────────────────────────────────────────────────────────
    sorted_r = sorted(advisor_results, key=lambda x: x.get("total_score", 0), reverse=True)
    above    = [r for r in sorted_r if r.get("total_score", 0) >= threshold]

    print(f"\n{'═' * 62}")
    print("📊  Reports saved:")
    print(f"    🌐  HTML    : {html_path}")
    print(f"    📦  JSON    : {json_path}")
    print(f"    💾  Outputs : {output_dir}/")
    print(f"\n🏁  DONE")
    print(f"    Screened  : {len(advisor_results)}")
    print(f"    Qualified : {len(above)} (score ≥ {threshold})")
    if sorted_r:
        best = sorted_r[0]
        print(f"    Top pick  : {best.get('candidate_name')} — {best.get('total_score')}/100 — {best.get('recommendation')}")
    print()


if __name__ == "__main__":
    main()
