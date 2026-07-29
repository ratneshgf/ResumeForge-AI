from fastapi import APIRouter, Depends

from app.core import session_store
from app.core.rate_limit import rate_limit
from app.schemas.job_description import JDAnalyzeRequest, JDAnalyzeResponse
from app.services.ai_engine.jd_analyzer import analyze

router = APIRouter(prefix="/api/v1/jd", tags=["job-description"])


@router.post("/analyze", response_model=JDAnalyzeResponse, dependencies=[Depends(rate_limit)])
async def analyze_jd(payload: JDAnalyzeRequest):
    result = analyze(payload.job_description)
    session_store.set_value(payload.session_id, "job_description", payload.job_description)
    session_store.set_value(payload.session_id, "jd_analysis", result)
    return JDAnalyzeResponse(**result)
