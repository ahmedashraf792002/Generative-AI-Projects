"""
agents/matcher.py — Job Requirements Matcher agent.
Scores ALL candidates against the job description in one batch call.
"""

from crewai import Agent, Task
from .models import MatchResult


def create_matcher_agent(llm) -> Agent:
    return Agent(
        role="Job Requirements Matcher",
        goal="Score how well each candidate matches the job requirements (0–100).",
        backstory=(
            "You are a technical recruiter specialising in AI/ML roles. "
            "You objectively score candidate-job fit based on skills, experience, "
            "education, and projects. Every score must be justified by evidence "
            "from the parsed resume — no charity points, no assumptions."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )


def create_match_task(
    agent: Agent,
    job_description: str,
    parse_task: Task,
) -> Task:
    return Task(
        description=f"""
You have received structured parsed data for ALL candidates from the previous task.
Score each candidate against the job description below.

━━━ JOB DESCRIPTION ━━━
{job_description}

━━━ SCORING RUBRIC (each dimension 0–25) ━━━

technical_skills (0–25)
  25 = all required skills + several nice-to-haves
  15 = most required skills covered
   8 = some required skills
   0 = missing almost all required skills

experience_level (0–25)
  25 = years and seniority perfectly match
  15 = slightly under/over required level
   8 = borderline relevant experience
   0 = no relevant experience

education_credentials (0–25)
  25 = required degree + relevant certs/publications
  15 = required degree, no extras
   8 = related but not exact degree
   0 = unrelated or missing degree

projects_portfolio (0–25)
  25 = multiple high-quality directly relevant projects
  15 = some relevant projects
   8 = generic or tangentially related
   0 = no projects or all irrelevant

total_score = sum of all 4 dimensions (0–100)

fit_verdict:
  80–100 → "Strong Fit"
  60–79  → "Good Fit"
  40–59  → "Partial Fit"
  0–39   → "Poor Fit"

━━━ OUTPUT FORMAT ━━━
Return ONLY a raw JSON array — one object per candidate, same order as parser output.
No markdown. No extra text. Start with [ end with ].

[
  {{
    "score_breakdown": {{
      "technical_skills": <0-25>,
      "experience_level": <0-25>,
      "education_credentials": <0-25>,
      "projects_portfolio": <0-25>
    }},
    "total_score": <0-100>,
    "strengths": ["...","...","..."],
    "gaps": ["...","...","..."],
    "fit_verdict": "Strong Fit | Good Fit | Partial Fit | Poor Fit"
  }}
]
""",
        agent=agent,
        expected_output="Raw JSON array of MatchResult objects, one per candidate.",
        context=[parse_task],
    )
