"""
agents/models.py — Pydantic output models for every agent.
Each model is the contract between an agent and the next stage in the pipeline.
"""

from typing import Literal
from pydantic import BaseModel, Field


# ── Screener ──────────────────────────────────────────────────────────────────

class ScreenResult(BaseModel):
    verdict: Literal["PASS", "FAIL"]
    reason: str
    matching_signals: list[str] = Field(default_factory=list)
    deal_breaker: str | None = None


# ── Parser ────────────────────────────────────────────────────────────────────

class Education(BaseModel):
    degree: str
    university: str
    gpa: str | None = None


class WorkHighlight(BaseModel):
    role: str
    company: str
    bullets: list[str]


class Project(BaseModel):
    name: str
    summary: str


class ParseResult(BaseModel):
    full_name: str
    email: str = ""
    contact_info: str = ""
    education: list[Education] = Field(default_factory=list)
    years_of_experience: float = 0.0
    technical_skills: list[str] = Field(default_factory=list)
    work_experience: list[WorkHighlight] = Field(default_factory=list)
    notable_projects: list[Project] = Field(default_factory=list)
    certifications_publications: list[str] = Field(default_factory=list)
    red_flags: list[str] = Field(default_factory=list)


# ── Matcher ───────────────────────────────────────────────────────────────────

class ScoreBreakdown(BaseModel):
    technical_skills: int = Field(ge=0, le=25)
    experience_level: int = Field(ge=0, le=25)
    education_credentials: int = Field(ge=0, le=25)
    projects_portfolio: int = Field(ge=0, le=25)


class MatchResult(BaseModel):
    score_breakdown: ScoreBreakdown
    total_score: int = Field(ge=0, le=100)
    strengths: list[str]
    gaps: list[str]
    fit_verdict: Literal["Strong Fit", "Good Fit", "Partial Fit", "Poor Fit"]


# ── Advisor ───────────────────────────────────────────────────────────────────

class AdvisorResult(BaseModel):
    candidate_name: str
    email: str = ""
    total_score: int = Field(ge=0, le=100)
    score_breakdown: ScoreBreakdown
    fit_verdict: Literal["Strong Fit", "Good Fit", "Partial Fit", "Poor Fit"]
    strengths: list[str]
    gaps: list[str]
    recommendation: Literal["Advance to Interview", "Consider with Reservations", "Reject"]
    suggested_interview_questions: list[str]
    hiring_notes: str


# ── Email Agent ───────────────────────────────────────────────────────────────

class EmailDraft(BaseModel):
    to: str
    subject: str
    body: str
    email_type: Literal["acceptance", "rejection"]
