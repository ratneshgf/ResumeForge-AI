import asyncio
import json
import threading
from unittest.mock import Mock

import httpx
import pytest

from app.main import app
from app.api.v1 import enhance
from app.core import session_store
from app.services.ai_engine import resume_enhancer
from app.services.ai_engine.client import AIClient, AIClientError


SECTIONS = [
    {"heading": "Contact", "paragraphs": [{"para_index": 0, "text": "Candidate contact information"}]},
    {"heading": "Experience", "paragraphs": [
        {"para_index": 1, "text": "Built Python APIs for customers."},
        {"para_index": 2, "text": "Maintained SQL databases."},
    ]},
]


def test_resume_uses_one_ai_call_and_preserves_paragraph_ids(monkeypatch):
    generate = Mock(return_value={"changes": [{"para_index": 2, "rewritten_text": "Maintained customer SQL databases."}]})
    monkeypatch.setattr(resume_enhancer, "generate_json", generate)
    changes = resume_enhancer.enhance_resume(SECTIONS, "Python developer")
    assert generate.call_count == 1
    payload = json.loads(generate.call_args.args[0].rsplit("\n", 1)[-1])
    assert [p["para_index"] for p in payload["paragraphs"]] == [1, 2]
    assert changes == [{"para_index": 2, "heading": "Experience", "before": "Maintained SQL databases.", "after": "Maintained customer SQL databases."}]


@pytest.mark.parametrize("changes", [
    [{"para_index": 0, "rewritten_text": "Changed private contact"}],
    [{"para_index": 999, "rewritten_text": "Unknown paragraph"}],
    [{"para_index": 1, "rewritten_text": ""}],
    [{"para_index": 1, "rewritten_text": "First"}, {"para_index": 1, "rewritten_text": "Duplicate"}],
])
def test_invalid_ai_changes_are_rejected(monkeypatch, changes):
    monkeypatch.setattr(resume_enhancer, "generate_json", lambda *args, **kwargs: {"changes": changes})
    with pytest.raises(AIClientError):
        resume_enhancer.enhance_resume(SECTIONS, "Python developer")


def test_quota_error_does_not_sleep(monkeypatch):
    from app.services.ai_engine import client
    monkeypatch.setattr(client.settings, "GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(client.settings, "AI_PROVIDER", "gemini")
    ai = AIClient()
    monkeypatch.setattr(ai, "_call_gemini", Mock(side_effect=AIClientError("RATE_LIMIT:60:429")))
    sleep = Mock()
    monkeypatch.setattr(client.time, "sleep", sleep)
    with pytest.raises(AIClientError, match="temporarily rate limited"):
        ai.generate_json("test")
    sleep.assert_not_called()


def test_health_remains_responsive_during_enhancement(monkeypatch):
    async def verify():
        started = threading.Event()
        release = threading.Event()
        def slow_enhance(*args):
            started.set()
            release.wait(5)
            return []
        monkeypatch.setattr(enhance, "enhance_resume", slow_enhance)
        session_store.set_value("concurrency-test", "sections", SECTIONS)
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            task = asyncio.create_task(client.post("/api/v1/enhance/full", json={"session_id": "concurrency-test", "resume_id": "test", "job_description": "Python developer"}))
            try:
                assert await asyncio.to_thread(started.wait, 2)
                assert not task.done()
                response = await asyncio.wait_for(client.get("/health"), timeout=1)
                assert response.status_code == 200
            finally:
                release.set()
                result = await task
                session_store.clear("concurrency-test")
            assert result.status_code == 200

    asyncio.run(verify())
