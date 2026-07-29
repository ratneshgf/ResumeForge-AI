"""
In-memory session store. Holds parsed resume schemas, source file paths,
and premium entitlement flags, keyed by session_id. No user accounts, no
database — matches the MVP's database-less design.

This is a SINGLE-PROCESS store: fine for local dev / a single uvicorn
worker. Running multiple workers or instances requires swapping this for
Redis (same get/set shape) since in-memory dicts aren't shared across
processes.
"""
from typing import Any

_store: dict[str, dict[str, Any]] = {}


def get(session_id: str) -> dict:
    return _store.setdefault(session_id, {})


def set_value(session_id: str, key: str, value: Any) -> None:
    _store.setdefault(session_id, {})[key] = value


def get_value(session_id: str, key: str, default=None) -> Any:
    return _store.get(session_id, {}).get(key, default)


def clear(session_id: str) -> None:
    _store.pop(session_id, None)
