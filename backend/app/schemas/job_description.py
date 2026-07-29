from pydantic import BaseModel


class JDAnalyzeRequest(BaseModel):
    session_id: str
    job_description: str


class JDAnalyzeResponse(BaseModel):
    required_skills: list[str]
    preferred_skills: list[str]
    keywords: list[str]
