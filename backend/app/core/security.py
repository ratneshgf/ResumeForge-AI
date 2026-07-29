"""
File upload validation. Checks magic bytes, not just extension, so a
renamed .exe can't slip through as ".docx".
"""
from fastapi import HTTPException, UploadFile

from app.config import settings

ALLOWED_TYPES = {
    "application/pdf": b"%PDF",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": b"PK",
}


async def validate_resume_file(file: UploadFile) -> bytes:
    contents = await file.read()

    size_mb = len(contents) / (1024 * 1024)
    if size_mb > settings.MAX_UPLOAD_MB:
        raise HTTPException(413, f"File exceeds {settings.MAX_UPLOAD_MB}MB limit")

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(415, "Only PDF and DOCX resumes are supported")

    magic = ALLOWED_TYPES[file.content_type]
    if not contents.startswith(magic):
        raise HTTPException(415, "File content does not match its declared type")

    return contents
