from pydantic import BaseModel


class RunStyle(BaseModel):
    bold: bool
    italic: bool
    size_pt: float | None
    color: str | None
    name: str | None


class RunModel(BaseModel):
    run_index: int
    text: str
    style: RunStyle


class ParagraphModel(BaseModel):
    para_index: int
    style_name: str
    text: str
    runs: list[RunModel]


class SectionModel(BaseModel):
    heading: str
    paragraphs: list[ParagraphModel]


class ResumeUploadResponse(BaseModel):
    session_id: str
    resume_id: str
    file_type: str
    sections: list[SectionModel]
