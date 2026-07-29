from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.core import session_store, storage
from app.core.rate_limit import rate_limit
from app.services.document_generator import docx_writer, pdf_writer

router = APIRouter(prefix="/api/v1/document", tags=["document"])


@router.post("/generate", dependencies=[Depends(rate_limit)])
async def generate_document(session_id: str):
    data = session_store.get(session_id)
    if "sections" not in data:
        raise HTTPException(404, "Upload and parse a resume for this session first")
    if "changes" not in data:
        raise HTTPException(400, "Run /enhance/full before generating the final document")

    ext = data["resume_ext"]
    out_dir = storage.output_dir(session_id)
    output_path = out_dir / f"enhanced.{ext}"

    if ext == "docx":
        docx_writer.apply_changes(data["resume_path"], str(output_path), data["changes"])
    else:
        pdf_writer.render(data["sections"], data["changes"], str(output_path))

    session_store.set_value(session_id, "output_path", str(output_path))
    return {"session_id": session_id, "file_type": ext, "ready": True}


@router.get("/download/{session_id}")
async def download_document(session_id: str):
    data = session_store.get(session_id)
    output_path = data.get("output_path")
    if not output_path:
        raise HTTPException(404, "No generated document for this session yet")

    ext = data["resume_ext"]
    media_type = (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        if ext == "docx" else "application/pdf"
    )
    return FileResponse(output_path, media_type=media_type, filename=f"resume_optimized.{ext}")
