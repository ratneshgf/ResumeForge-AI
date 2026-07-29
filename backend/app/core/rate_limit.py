"""
Minimal in-memory rate limiter. Fine for a single-instance MVP; swap for a
Redis-backed limiter (e.g. slowapi + Redis) once you run multiple workers.
"""
import time
from collections import defaultdict

from fastapi import HTTPException, Request

from app.config import settings

_hits: dict[str, list[float]] = defaultdict(list)


def rate_limit(request: Request) -> None:
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    window_start = now - 60
    _hits[ip] = [t for t in _hits[ip] if t > window_start]

    if len(_hits[ip]) >= settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(429, "Too many requests — please slow down")

    _hits[ip].append(now)
