"""
agents/parser.py — Resume Parser agent.
Extracts structured data from ALL resumes in one batch call.
"""

from crewai import Agent, Task
from .models import ParseResult


def create_parser_agent(llm) -> Agent:
    return Agent(
        role="Resume Parser",
        goal="Extract structured, accurate information from candidate resumes.",
        backstory=(
            "You are a meticulous HR analyst with 10 years of experience parsing "
            "tech and AI/ML resumes. You extract only what is explicitly stated — "
            "never invent or assume. If a field is absent, you write an empty value."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )


def create_parse_task(
    agent: Agent,
    all_resumes: dict[str, str],  # {candidate_name: resume_text}
) -> Task:
    resumes_block = ""
    for name, text in all_resumes.items():
        resumes_block += f"\n\n=== CANDIDATE: {name} ===\n{text}\n"

    return Task(
        description=f"""
Parse ALL of the following resumes. For EACH candidate extract every field below.
Do NOT invent or assume anything not explicitly stated.

━━━ RESUMES ━━━
{resumes_block}

━━━ FIELDS TO EXTRACT PER CANDIDATE ━━━
1. full_name          — exact name as written
2. email              — email address only (empty string if not found)
3. contact_info       — all contact details as one comma-separated string
4. education          — list of {{degree, university, gpa(null if missing)}}
5. years_of_experience — total professional years as float
6. technical_skills   — all languages, frameworks, tools mentioned
7. work_experience    — per role: {{role, company, bullets(max 3)}}
8. notable_projects   — per project: {{name, summary(one line)}}
9. certifications_publications — list of certs, courses, papers ([] if none)
10. red_flags         — gaps >6 months, vague roles, no relevant experience

━━━ OUTPUT FORMAT ━━━
Return ONLY a raw JSON array — one object per candidate, same order as input.
No markdown. No extra text. Start with [ and end with ].

[
  {{
    "full_name": "...",
    "email": "...",
    "contact_info": "...",
    "education": [{{"degree":"...","university":"...","gpa":null}}],
    "years_of_experience": 2.5,
    "technical_skills": ["Python","PyTorch"],
    "work_experience": [{{"role":"...","company":"...","bullets":["..."]}}],
    "notable_projects": [{{"name":"...","summary":"..."}}],
    "certifications_publications": [],
    "red_flags": []
  }}
]
""",
        agent=agent,
        expected_output="Raw JSON array of ParseResult objects, one per candidate.",
    )
