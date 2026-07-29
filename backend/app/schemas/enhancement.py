from pydantic import BaseModel


class EnhanceRequest(BaseModel):
    session_id: str
    resume_id: str
    job_description: str
    premium: bool = False


class SectionChange(BaseModel):
    para_index: int
    heading: str
    before: str
    after: str


class EnhanceResponse(BaseModel):
    session_id: str
    resume_id: str
    changes: list[SectionChange]
