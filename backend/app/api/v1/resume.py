import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core import session_store, storage
from app.core.rate_limit import rate_limit
from app.core.security import validate_resume_file
from app.schemas.resume import ResumeUploadResponse
from app.services.resume_parser import docx_extractor, pdf_extractor

router = APIRouter(prefix="/api/v1/resume", tags=["resume"])


@router.post("/upload", response_model=ResumeUploadResponse, dependencies=[Depends(rate_limit)])
async def upload_resume(file: UploadFile = File(...)):
    contents = await validate_resume_file(file)

    session_id = storage.new_session_id()
    resume_id = uuid.uuid4().hex
    is_pdf = file.content_type == "application/pdf"
    ext = "pdf" if is_pdf else "docx"

    upload_path = storage.upload_dir(session_id) / f"{resume_id}.{ext}"
    upload_path.write_bytes(contents)

    try:
        parsed = pdf_extractor.extract(str(upload_path)) if is_pdf else docx_extractor.extract(str(upload_path))
    except Exception as exc:
        raise HTTPException(422, f"Could not parse resume: {exc}")

    session_store.set_value(session_id, "resume_id", resume_id)
    session_store.set_value(session_id, "resume_path", str(upload_path))
    session_store.set_value(session_id, "resume_ext", ext)
    session_store.set_value(session_id, "sections", parsed["sections"])

    return ResumeUploadResponse(
        session_id=session_id,
        resume_id=resume_id,
        file_type=ext,
        sections=parsed["sections"],
    )


@router.get("/{session_id}", response_model=ResumeUploadResponse)
async def get_parsed_resume(session_id: str):
    data = session_store.get(session_id)
    if "sections" not in data:
        raise HTTPException(404, "No parsed resume found for this session")
    return ResumeUploadResponse(
        session_id=session_id,
        resume_id=data["resume_id"],
        file_type=data["resume_ext"],
        sections=data["sections"],
    )
