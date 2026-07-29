"""
Ephemeral file storage. No database — every upload/output lives under a
session_id directory that gets purged after FILE_TTL_MINUTES.
"""
import shutil
import time
import uuid
from pathlib import Path

from app.config import settings

BASE = Path(__file__).resolve().parents[2]  # backend/


def _dir(base_name: str, session_id: str) -> Path:
    path = BASE / getattr(settings, base_name) / session_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def new_session_id() -> str:
    return uuid.uuid4().hex


def upload_dir(session_id: str) -> Path:
    return _dir("UPLOAD_DIR", session_id)


def temp_dir(session_id: str) -> Path:
    return _dir("TEMP_DIR", session_id)


def output_dir(session_id: str) -> Path:
    return _dir("OUTPUT_DIR", session_id)


def purge_expired() -> int:
    """Delete session directories older than FILE_TTL_MINUTES. Returns count removed."""
    cutoff = time.time() - settings.FILE_TTL_MINUTES * 60
    removed = 0
    for base_name in ("UPLOAD_DIR", "TEMP_DIR", "OUTPUT_DIR"):
        root = BASE / getattr(settings, base_name)
        if not root.exists():
            continue
        for session_path in root.iterdir():
            if session_path.is_dir() and session_path.stat().st_mtime < cutoff:
                shutil.rmtree(session_path, ignore_errors=True)
                removed += 1
    return removed


def purge_session(session_id: str) -> None:
    for base_name in ("UPLOAD_DIR", "TEMP_DIR", "OUTPUT_DIR"):
        path = BASE / getattr(settings, base_name) / session_id
        shutil.rmtree(path, ignore_errors=True)
