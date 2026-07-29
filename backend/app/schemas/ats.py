from pydantic import BaseModel
from typing import Dict, Optional


class ATSScoreRequest(BaseModel):
    session_id: str
    resume_id: str
    job_description: str


class ScoreBreakdown(BaseModel):
    skill_match: int
    keyword_match: int
    semantic_similarity: int
    experience_match: int
    education_match: int
    completeness: int


class ExperienceYears(BaseModel):
    required: int
    found: int


class Education(BaseModel):
    required: str
    found: str


class ATSScoreResponse(BaseModel):
    score: int
    breakdown: ScoreBreakdown
    skills_match_pct: int
    keyword_match_pct: int
    matched_skills: list[str]
    missing_skills: list[str]
    matched_keywords: Optional[list[str]] = []
    missing_keywords: Optional[list[str]] = []
    suggestions: list[str]
    completeness_check: Optional[Dict[str, bool]] = {}
    experience_years: Optional[ExperienceYears] = None
    education: Optional[Education] = None
    error: Optional[str] = None
