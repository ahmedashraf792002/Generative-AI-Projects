"""
agents/advisor.py — Senior Hiring Advisor agent.
Synthesises parser + matcher outputs into final recommendations for ALL candidates.
"""

from crewai import Agent, Task
from .models import AdvisorResult


def create_advisor_agent(llm) -> Agent:
    return Agent(
        role="Senior Hiring Advisor",
        goal="Produce final hiring recommendations for all candidates with actionable insights.",
        backstory=(
            "You are a C-level hiring consultant who synthesises resume parsing and "
            "scoring into clear, unbiased recommendations. "
            "You output valid JSON only — never markdown, never preamble."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )


def create_advise_task(
    agent: Agent,
    candidate_names: list[str],
    parse_task: Task,
    match_task: Task,
) -> Task:
    names_list = "\n".join(f"  {i+1}. {n}" for i, n in enumerate(candidate_names))

    return Task(
        description=f"""
Using ALL outputs from the parser and matcher tasks, produce a FINAL HIRING
RECOMMENDATION for EACH of the following candidates:

{names_list}

━━━ RULES ━━━
- Carry forward scores from the matcher — do NOT recalculate.
- total_score MUST equal the exact sum of the four score_breakdown values.
- recommendation logic (strictly follow this):
    total_score >= 75  → "Advance to Interview"
    total_score 50–74  → "Consider with Reservations"
    total_score < 50   → "Reject"
- Craft 3 interview questions that specifically probe the identified gaps.
- hiring_notes: 2–3 sentences a busy hiring manager can act on immediately.
- Include the candidate's email from the parser output in each object.

━━━ OUTPUT FORMAT ━━━
Return ONLY a raw JSON array — one object per candidate, same order as input list.
No markdown. No extra text. Start with [ end with ].

[
  {{
    "candidate_name": "...",
    "email": "...",
    "total_score": <0-100>,
    "score_breakdown": {{
      "technical_skills": <0-25>,
      "experience_level": <0-25>,
      "education_credentials": <0-25>,
      "projects_portfolio": <0-25>
    }},
    "fit_verdict": "Strong Fit | Good Fit | Partial Fit | Poor Fit",
    "strengths": ["...","...","..."],
    "gaps": ["...","...","..."],
    "recommendation": "Advance to Interview | Consider with Reservations | Reject",
    "suggested_interview_questions": ["...","...","..."],
    "hiring_notes": "..."
  }}
]
""",
        agent=agent,
        expected_output="Raw JSON array of AdvisorResult objects, one per candidate.",
        context=[parse_task, match_task],
    )
