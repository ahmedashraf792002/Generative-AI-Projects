"""
agents/email_agent.py — Email Drafter agent.

Drafts personalised emails for ALL candidates in one pass:
  - Accepted  → warm congratulations, interview availability, next steps
  - Rejected  → empathetic, respectful, encourages future applications
  - On Hold   → acknowledges receipt, explains review continues

Also provides send_email() for actual SMTP delivery when credentials are configured.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from crewai import Agent, Task
from .models import EmailDraft


def create_email_agent(llm) -> Agent:
    return Agent(
        role="Talent Communications Specialist",
        goal="Draft professional, empathetic, personalised emails for all candidates.",
        backstory=(
            "You are a senior talent acquisition specialist known for writing emails "
            "that make accepted candidates feel genuinely excited and rejected candidates "
            "feel respected. Your emails are warm, specific, and professional. "
            "You never use generic copy-paste templates — every email references "
            "something specific to the candidate."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )


def create_email_task(
    agent: Agent,
    candidates: list[dict],  # list of advisor result dicts
    position: str,
    company_name: str,
    interview_slots: str = "Monday–Thursday, 10 AM – 4 PM",
) -> Task:
    candidates_block = ""
    for c in candidates:
        candidates_block += f"""
--- {c['candidate_name']} ---
Email        : {c.get('email', 'unknown')}
Score        : {c.get('total_score', 0)}/100
Verdict      : {c.get('fit_verdict', '')}
Recommendation: {c.get('recommendation', '')}
Strengths    : {', '.join(c.get('strengths', [])[:2])}
Gaps         : {', '.join(c.get('gaps', [])[:2])}
Notes        : {c.get('hiring_notes', '')}
"""

    return Task(
        description=f"""
Draft a personalised email for EACH candidate listed below.

Position : {position}
Company  : {company_name}
Interview availability (for accepted): {interview_slots}

━━━ CANDIDATES ━━━
{candidates_block}

━━━ EMAIL RULES ━━━

ACCEPTED ("Advance to Interview"):
  Subject: "Exciting News — Interview Invitation for [Position] at [Company]"
  Body must include:
  - Warm congratulations referencing ONE specific strength
  - Clear next steps: schedule interview, interview availability window
  - Brief note on what to expect in the interview (technical + culture fit)
  - Professional sign-off

REJECTED ("Reject"):
  Subject: "Your Application for [Position] at [Company]"
  Body must include:
  - Genuine thank-you for their time and application
  - Empathetic regret message (do NOT say "we went with a more qualified candidate")
  - One genuine encouragement referencing something positive you saw
  - Invitation to apply for future roles
  - Professional sign-off

ON HOLD ("Consider with Reservations"):
  Subject: "Your Application for [Position] at [Company] — Update"
  Body must include:
  - Thank-you for their patience
  - Honest message that evaluation is ongoing
  - Expected timeline ("we aim to reach out within 2 weeks")
  - Professional sign-off

━━━ OUTPUT FORMAT ━━━
Return ONLY a raw JSON array — one object per candidate, same order as input.
No markdown. No extra text. Start with [ end with ].

[
  {{
    "to": "<email address>",
    "subject": "<subject line>",
    "body": "<full email body — use \\n for line breaks>",
    "email_type": "acceptance | rejection | on_hold"
  }}
]
""",
        agent=agent,
        expected_output="Raw JSON array of email drafts, one per candidate.",
    )


# ── SMTP sender ───────────────────────────────────────────────────────────────

def send_email(draft: dict, smtp_config: dict | None = None) -> bool:
    """
    Send a single email draft via SMTP.
    smtp_config keys: host, port, user, password, from_name
    Falls back to env vars: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD.
    Returns True on success, False on failure.
    """
    cfg = smtp_config or {}
    host     = cfg.get("host")     or os.getenv("SMTP_HOST", "")
    port     = int(cfg.get("port") or os.getenv("SMTP_PORT", 587))
    user     = cfg.get("user")     or os.getenv("SMTP_USER", "")
    password = cfg.get("password") or os.getenv("SMTP_PASSWORD", "")
    from_name = cfg.get("from_name") or os.getenv("SMTP_FROM_NAME", "Hiring Team")

    if not all([host, user, password, draft.get("to")]):
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = draft["subject"]
    msg["From"]    = f"{from_name} <{user}>"
    msg["To"]      = draft["to"]
    msg.attach(MIMEText(draft["body"], "plain", "utf-8"))

    try:
        with smtplib.SMTP(host, port) as server:
            server.ehlo()
            server.starttls()
            server.login(user, password)
            server.sendmail(user, draft["to"], msg.as_string())
        return True
    except Exception as e:
        print(f"    ✉️  SMTP error sending to {draft['to']}: {e}")
        return False
