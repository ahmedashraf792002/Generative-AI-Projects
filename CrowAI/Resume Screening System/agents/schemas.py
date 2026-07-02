"""
agents/schemas.py
─────────────────
Pydantic v2 schemas for ALL agent outputs in the Resume Screening System.

Usage:
    from agents.schemas import HiringDecision, ScreeningReport, ParsedResume

Every agent output is validated against these schemas before being saved
or passed to the next agent. This guarantees:
  • Type safety  — scores are ints, not strings
  • Range checks — scores are clamped 0-100
  • Consistency  — total_score always == sum of breakdown
  • Enum safety  — verdict/recommendation always a known value
"""

from __future__ import annotations

import re
from datetime import datetime
from enum import Enum
from typing import Optional, Literal
import json
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    computed_field,
    field_validator,
    model_validator,
)


# ══════════════════════════════════════════════════════════════════════════════
#  ENUMS — locked vocabulary, prevents LLM from inventing new values
# ══════════════════════════════════════════════════════════════════════════════

class FitVerdict(str, Enum):
    STRONG  = "Strong Fit"
    GOOD    = "Good Fit"
    PARTIAL = "Partial Fit"
    POOR    = "Poor Fit"


class Recommendation(str, Enum):
    ADVANCE  = "Advance to Interview"
    CONSIDER = "Consider with Reservations"
    REJECT   = "Reject"


class EmailAction(str, Enum):
    SEND_ACCEPTED = "send_accepted"
    SEND_REJECTED = "send_rejected"
    HOLD          = "hold"


class EmailStatus(str, Enum):
    SENT     = "sent"
    DRY_RUN  = "dry_run"
    HELD     = "held"
    NO_EMAIL = "no_email"
    FAILED   = "failed"
    DISABLED = "disabled"


class BudgetFit(str, Enum):
    WITHIN = "within"
    ABOVE  = "above"
    BELOW  = "below"


class RiskLevel(str, Enum):
    LOW    = "low"
    MEDIUM = "medium"
    HIGH   = "high"


class InterviewType(str, Enum):
    VIDEO  = "video"
    PHONE  = "phone"
    ONSITE = "onsite"


# ══════════════════════════════════════════════════════════════════════════════
#  AGENT 0: SCREENER OUTPUT
# ══════════════════════════════════════════════════════════════════════════════

class ScreenerOutput(BaseModel):
    """Gate-keeper — runs before parser to reject junk files."""

    is_valid_resume: bool
    language_detected: str                         = "Unknown"
    relevance_score: int                           = Field(0, ge=0, le=10)
    rejection_reason: Optional[str]                = None
    proceed_to_parse: bool                         = True

    @model_validator(mode="after")
    def sync_proceed(self) -> "ScreenerOutput":
        if not self.is_valid_resume or self.relevance_score < 2:
            object.__setattr__(self, "proceed_to_parse", False)
        return self


# ══════════════════════════════════════════════════════════════════════════════
#  AGENT 1: PARSER OUTPUT
# ══════════════════════════════════════════════════════════════════════════════

class ContactInfo(BaseModel):
    full_name: str
    email: Optional[EmailStr]   = None
    phone: Optional[str]        = None
    linkedin: Optional[str]     = None
    github: Optional[str]       = None
    location: Optional[str]     = None

    @field_validator("phone", mode="before")
    @classmethod
    def clean_phone(cls, v):
        if v is None:
            return None
        digits = re.sub(r"[^\d+]", "", str(v))
        return digits if len(digits) >= 7 else None


class Education(BaseModel):
    degree: str
    major: str                  = "Not mentioned"
    university: str
    graduation_year: Optional[int] = None
    gpa: Optional[float]        = Field(None, ge=0.0, le=4.0)

    @field_validator("gpa", mode="before")
    @classmethod
    def parse_gpa(cls, v):
        if v is None or str(v).lower() in ("not mentioned", "n/a", ""):
            return None
        try:
            return float(v)
        except (ValueError, TypeError):
            return None


class WorkExperience(BaseModel):
    title: str
    company: str
    start_date: str             = "Unknown"
    end_date: str               = "Present"
    achievements: list[str]     = Field(default_factory=list, max_length=5)


class Project(BaseModel):
    name: str
    tech_stack: list[str]       = Field(default_factory=list)
    outcome: str                = "Not mentioned"
    url: Optional[str]          = None


class ParsedResume(BaseModel):
    """Complete structured output from the Parser agent."""

    contact: ContactInfo
    education: list[Education]                = Field(default_factory=list)
    experience: list[WorkExperience]          = Field(default_factory=list)
    total_years_experience: float             = Field(0.0, ge=0.0)
    technical_skills: list[str]               = Field(default_factory=list)
    projects: list[Project]                   = Field(default_factory=list)
    certifications: list[str]                 = Field(default_factory=list)
    publications: list[str]                   = Field(default_factory=list)
    soft_skills: list[str]                    = Field(default_factory=list)
    languages_spoken: list[str]               = Field(default_factory=list)
    red_flags: list[str]                      = Field(default_factory=list)

    @computed_field
    @property
    def has_contact_email(self) -> bool:
        return self.contact.email is not None

    @computed_field
    @property
    def skill_count(self) -> int:
        return len(self.technical_skills)


# ══════════════════════════════════════════════════════════════════════════════
#  AGENT 1.5: FACT-CHECKER OUTPUT (new — between Parser and Matcher)
# ══════════════════════════════════════════════════════════════════════════════

class FactCheckOutput(BaseModel):
    """
    Cross-validates claimed skills vs. actual evidence in the resume.
    Biggest accuracy improvement: prevents keyword-stuffed resumes from
    scoring high on technical skills.
    """

    verified_skills: list[str]      = Field(default_factory=list)
    unverified_claims: list[str]    = Field(default_factory=list)
    inconsistencies: list[str]      = Field(default_factory=list)
    credibility_score: int          = Field(100, ge=0, le=100)
    red_flags: list[str]            = Field(default_factory=list)
    penalty_points: int             = Field(0, ge=0, le=20)

    @computed_field
    @property
    def is_credible(self) -> bool:
        return self.credibility_score >= 60 and self.penalty_points <= 10


# ══════════════════════════════════════════════════════════════════════════════
#  AGENT 2: MATCHER OUTPUT
# ══════════════════════════════════════════════════════════════════════════════

class ScoreBreakdown(BaseModel):
    technical_skills: int       = Field(0, ge=0, le=25)
    experience_level: int       = Field(0, ge=0, le=25)
    education_credentials: int  = Field(0, ge=0, le=25)
    projects_portfolio: int     = Field(0, ge=0, le=25)

    @computed_field
    @property
    def total(self) -> int:
        return (
            self.technical_skills
            + self.experience_level
            + self.education_credentials
            + self.projects_portfolio
        )


class MatchResult(BaseModel):
    """Scored output from the Matcher agent."""

    score: ScoreBreakdown
    verdict: FitVerdict
    strengths: list[str]        = Field(default_factory=list, max_length=5)
    gaps: list[str]             = Field(default_factory=list, max_length=5)
    evidence: dict[str, str]    = Field(default_factory=dict)

    @computed_field
    @property
    def total_score(self) -> int:
        return self.score.total


# ══════════════════════════════════════════════════════════════════════════════
#  AGENT 2.5: BIAS DETECTOR OUTPUT (new)
# ══════════════════════════════════════════════════════════════════════════════

class BiasCheckOutput(BaseModel):
    """
    Detects if the Matcher score was influenced by irrelevant factors:
    university prestige, employment gaps (e.g. military service),
    gender signals, or degree type bias.
    """

    bias_detected: bool                 = False
    bias_types: list[str]               = Field(default_factory=list)
    adjusted_score: Optional[int]       = Field(None, ge=0, le=100)
    score_delta: int                    = 0
    explanation: str                    = "No bias detected."
    military_service_gap_detected: bool = False


# ══════════════════════════════════════════════════════════════════════════════
#  AGENT 2.6: SALARY ESTIMATOR OUTPUT (new)
# ══════════════════════════════════════════════════════════════════════════════

class SalaryOutput(BaseModel):
    """Estimates salary expectation and flags budget mismatch."""

    estimated_min: int          = Field(0, ge=0)
    estimated_max: int          = Field(0, ge=0)
    stated_expectation: Optional[int]   = None
    budget_fit: BudgetFit       = BudgetFit.WITHIN
    overqualified_risk: bool    = False
    market: str                 = "Egypt local"
    currency: str               = "USD"
    notes: str                  = ""

    @model_validator(mode="after")
    def validate_range(self) -> "SalaryOutput":
        if self.estimated_max < self.estimated_min:
            object.__setattr__(self, "estimated_max", self.estimated_min)
        return self


# ══════════════════════════════════════════════════════════════════════════════
#  AGENT 3: ADVISOR OUTPUT  (HiringDecision — the master output)
# ══════════════════════════════════════════════════════════════════════════════

class HiringDecision(BaseModel):
    """
    Final structured output from the Advisor agent.
    This is the ground truth used for the HTML report, email agent,
    and saved JSON file.
    """

    candidate_name: str
    email: Optional[EmailStr]               = None
    phone: Optional[str]                    = None
    location: Optional[str]                 = None

    total_score: int                        = Field(0, ge=0, le=100)
    score_breakdown: ScoreBreakdown
    credibility_score: Optional[int]        = Field(None, ge=0, le=100)
    bias_adjusted_score: Optional[int]      = Field(None, ge=0, le=100)

    fit_verdict: FitVerdict
    strengths: list[str]                    = Field(default_factory=list)
    gaps: list[str]                         = Field(default_factory=list)
    recommendation: Recommendation
    suggested_interview_questions: list[str] = Field(default_factory=list)
    hiring_notes: str                       = ""
    call_availability: str                  = "Available for call immediately"
    email_action: EmailAction               = EmailAction.HOLD
    confidence: int                         = Field(80, ge=0, le=100)

    source_file: str                        = ""
    email_status: Optional[str]             = None
    email_sent_at: Optional[str]            = None

    @model_validator(mode="after")
    def check_score_consistency(self) -> "HiringDecision":
        computed = self.score_breakdown.total
        if computed != self.total_score:
            object.__setattr__(self, "total_score", computed)
        return self

    @model_validator(mode="after")
    def infer_email_action(self) -> "HiringDecision":
        if self.email_action == EmailAction.HOLD:
            if self.recommendation == Recommendation.ADVANCE:
                object.__setattr__(self, "email_action", EmailAction.SEND_ACCEPTED)
            elif self.recommendation == Recommendation.REJECT:
                object.__setattr__(self, "email_action", EmailAction.SEND_REJECTED)
        return self

    @computed_field
    @property
    def passed_threshold(self) -> bool:
        import os
        t = int(os.getenv("MIN_SCORE_THRESHOLD", 60))
        return self.total_score >= t

    def to_dict(self) -> dict:
        """Serialise to plain dict for JSON / report."""
        d = self.model_dump(mode="json")
        d["fit_verdict"]    = self.fit_verdict.value
        d["recommendation"] = self.recommendation.value
        d["email_action"]   = self.email_action.value
        d["total_score"]    = self.total_score
        return d


# ══════════════════════════════════════════════════════════════════════════════
#  AGENT 4: EMAIL LOG
# ══════════════════════════════════════════════════════════════════════════════

class EmailLog(BaseModel):
    """Saved output from the Email agent."""

    candidate_name: str
    to_email: Optional[EmailStr]    = None
    action: EmailAction
    subject: str                    = ""
    body: str                       = ""
    status: EmailStatus
    sent_at: Optional[datetime]     = None
    error: Optional[str]            = None


# ══════════════════════════════════════════════════════════════════════════════
#  AGENT 5: SCHEDULER OUTPUT (new)
# ══════════════════════════════════════════════════════════════════════════════

class SchedulerOutput(BaseModel):
    """Interview slot proposal — runs after acceptance email."""

    candidate_name: str
    proposed_slots: list[str]           = Field(default_factory=list, max_length=3)
    confirmed_slot: Optional[str]       = None
    interview_type: InterviewType       = InterviewType.VIDEO
    calendar_event_created: bool        = False
    notes: str                          = ""


# ══════════════════════════════════════════════════════════════════════════════
#  AGENT 6: SUMMARY REPORTER OUTPUT (new)
# ══════════════════════════════════════════════════════════════════════════════

class SummaryOutput(BaseModel):
    """Human-readable prose summary for the hiring manager."""

    candidate_name: str
    executive_summary: str          = Field(..., max_length=800)
    one_line_verdict: str           = Field(..., max_length=120)
    risk_level: RiskLevel           = RiskLevel.MEDIUM
    confidence: int                 = Field(80, ge=0, le=100)

    @field_validator("executive_summary")
    @classmethod
    def summary_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("executive_summary cannot be empty")
        return v.strip()


# ══════════════════════════════════════════════════════════════════════════════
#  TOP-LEVEL REPORT SCHEMA
# ══════════════════════════════════════════════════════════════════════════════

class ScreeningReport(BaseModel):
    """
    Master report wrapping all candidates' HiringDecision objects.
    Saved as results/results_TIMESTAMP.json after each run.
    """

    job_title: str
    company: str
    generated_at: datetime              = Field(default_factory=datetime.now)
    llm_provider: Literal["openai", "ollama"]
    llm_model: str
    total_candidates: int               = 0
    threshold: int                      = Field(60, ge=0, le=100)
    decisions: list[HiringDecision]     = Field(default_factory=list)

    @computed_field
    @property
    def top_candidates(self) -> list[str]:
        return [
            d.candidate_name
            for d in sorted(self.decisions, key=lambda x: x.total_score, reverse=True)
            if d.total_score >= self.threshold
        ]

    @computed_field
    @property
    def pass_rate(self) -> float:
        if not self.decisions:
            return 0.0
        above = sum(1 for d in self.decisions if d.total_score >= self.threshold)
        return round(above / len(self.decisions) * 100, 1)

    @computed_field
    @property
    def avg_score(self) -> float:
        if not self.decisions:
            return 0.0
        return round(sum(d.total_score for d in self.decisions) / len(self.decisions), 1)

    def to_json_safe(self) -> list[dict]:
        """Return list of plain dicts sorted by score (for report.py)."""
        return sorted(
            [d.to_dict() for d in self.decisions],
            key=lambda x: x.get("total_score", 0),
            reverse=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
#  UTILITY: safe JSON → HiringDecision
# ══════════════════════════════════════════════════════════════════════════════

def _normalize_enum_value(value, enum_cls, default):
    """Map loose/incorrect LLM strings onto the closest valid enum value."""
    if value is None:
        return default.value
    v = str(value).strip().lower()

    # Exact match first
    for member in enum_cls:
        if v == member.value.lower():
            return member.value

    # Fuzzy keyword matching per enum type
    if enum_cls is Recommendation:
        if any(k in v for k in ("advance", "interview", "accept", "yes", "proceed", "hire")):
            return Recommendation.ADVANCE.value
        if any(k in v for k in ("reject", "no", "decline", "pass")):
            return Recommendation.REJECT.value
        return Recommendation.CONSIDER.value

    if enum_cls is FitVerdict:
        if "strong" in v: return FitVerdict.STRONG.value
        if "good" in v:   return FitVerdict.GOOD.value
        if "poor" in v or "weak" in v or "bad" in v: return FitVerdict.POOR.value
        return FitVerdict.PARTIAL.value

    if enum_cls is EmailAction:
        if "accept" in v: return EmailAction.SEND_ACCEPTED.value
        if "reject" in v: return EmailAction.SEND_REJECTED.value
        return EmailAction.HOLD.value

    return default.value


def _clamp(value, lo, hi, default=0):
    try:
        n = int(round(float(value)))
    except (TypeError, ValueError):
        return default
    return max(lo, min(hi, n))


def _clean_email(value):
    """Return a valid-looking email or None — avoids EmailStr validation crashes."""
    if not value or not isinstance(value, str):
        return None
    v = value.strip()
    if not v or v.lower() in ("none", "null", "n/a", "not mentioned", "not provided"):
        return None
    if re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
        return v
    return None


def parse_hiring_decision(raw: str | dict, fallback_name: str = "Unknown") -> HiringDecision:
    """
    Parse raw LLM output (string or dict) into a validated HiringDecision.
    Normalizes field-by-field instead of discarding the whole object on
    a single bad field, so partial/imperfect LLM output is still usable.
    """
    import json as _json

    if isinstance(raw, str):
        candidates = _extract_balanced_json(raw)
        parsed = None
        for c in candidates:
            try:
                d = _json.loads(c)
                if isinstance(d, dict):
                    parsed = d
                    break
            except json.JSONDecodeError:
                continue
        raw = parsed or {}

    if not isinstance(raw, dict):
        raw = {}

    notes_prefix = ""
    if not raw:
        notes_prefix = "⚠️ No valid JSON found in agent output — used defaults. "

    # ── candidate_name ──────────────────────────────────────────────────────
    name = raw.get("candidate_name") or fallback_name

    # ── score_breakdown (clamp each dimension into 0-25) ────────────────────
    bd_raw = raw.get("score_breakdown") or {}
    if not isinstance(bd_raw, dict):
        bd_raw = {}
    if not bd_raw:
        # Derive an even split from total_score if breakdown missing
        ts = _clamp(raw.get("total_score", 0), 0, 100)
        q = ts // 4
        bd_raw = {
            "technical_skills": q,
            "experience_level": q,
            "education_credentials": q,
            "projects_portfolio": ts - 3 * q,
        }
    score_breakdown = ScoreBreakdown(
        technical_skills=_clamp(bd_raw.get("technical_skills", 0), 0, 25),
        experience_level=_clamp(bd_raw.get("experience_level", 0), 0, 25),
        education_credentials=_clamp(bd_raw.get("education_credentials", 0), 0, 25),
        projects_portfolio=_clamp(bd_raw.get("projects_portfolio", 0), 0, 25),
    )

    # ── enums (fuzzy-normalized so a single bad string doesn't nuke the result)
    fit_verdict    = _normalize_enum_value(raw.get("fit_verdict"), FitVerdict, FitVerdict.PARTIAL)
    recommendation = _normalize_enum_value(raw.get("recommendation"), Recommendation, Recommendation.CONSIDER)
    email_action    = _normalize_enum_value(raw.get("email_action"), EmailAction, EmailAction.HOLD)

    # ── lists (coerce non-lists into empty list rather than crash) ──────────
    def _as_list(v):
        if isinstance(v, list):
            return [str(x) for x in v]
        if isinstance(v, str) and v.strip():
            return [v.strip()]
        return []

    payload = {
        "candidate_name": str(name),
        "email": _clean_email(raw.get("email")),
        "phone": raw.get("phone") if isinstance(raw.get("phone"), str) else None,
        "location": raw.get("location") if isinstance(raw.get("location"), str) else None,
        "total_score": score_breakdown.total,
        "score_breakdown": score_breakdown,
        "credibility_score": (
            _clamp(raw["credibility_score"], 0, 100) if raw.get("credibility_score") is not None else None
        ),
        "fit_verdict": fit_verdict,
        "strengths": _as_list(raw.get("strengths")),
        "gaps": _as_list(raw.get("gaps")),
        "recommendation": recommendation,
        "suggested_interview_questions": _as_list(raw.get("suggested_interview_questions")),
        "hiring_notes": notes_prefix + str(raw.get("hiring_notes") or ""),
        "call_availability": str(raw.get("call_availability") or "Available for call immediately"),
        "email_action": email_action,
        "confidence": _clamp(raw.get("confidence", 80), 0, 100, default=80),
    }

    try:
        return HiringDecision(**payload)
    except Exception as e:
        # Should be extremely rare now — every field above is pre-sanitized.
        return HiringDecision(
            candidate_name=str(name),
            total_score=score_breakdown.total,
            score_breakdown=score_breakdown,
            fit_verdict=FitVerdict.PARTIAL,
            recommendation=Recommendation.CONSIDER,
            hiring_notes=f"⚠️ Partial validation issue (data preserved where possible): {e}",
        )


def _extract_balanced_json(raw: str) -> list[str]:
    """Brace-depth matched JSON object extraction (handles nested braces)."""
    raw = re.sub(r"```(?:json)?", "", str(raw))
    candidates, depth, start = [], 0, None
    for i, ch in enumerate(raw):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    candidates.append(raw[start:i + 1])
                    start = None
    candidates.sort(key=len, reverse=True)
    return candidates