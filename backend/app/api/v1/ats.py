import logging
from fastapi import APIRouter, Depends, HTTPException

from app.core import session_store
from app.core.rate_limit import rate_limit
from app.schemas.ats import ATSScoreRequest, ATSScoreResponse
from app.services.ai_engine.ats_scorer import score as score_resume

router = APIRouter(prefix="/api/v1/ats", tags=["ats"])
logger = logging.getLogger(__name__)


@router.post("/score", response_model=ATSScoreResponse, dependencies=[Depends(rate_limit)])
async def get_ats_score(payload: ATSScoreRequest):
    data = session_store.get(payload.session_id)
    if "sections" not in data:
        raise HTTPException(404, "Upload and parse a resume for this session first")

    try:
        logger.info(f"Computing ATS score for session {payload.session_id}")
        result = score_resume(data["sections"], payload.job_description)
        logger.info(f"ATS score computed: {result['score']}")
        return ATSScoreResponse(**result)
    
    except Exception as e:
        logger.error(f"ATS scoring error: {e}", exc_info=True)
        raise HTTPException(500, f"Error computing ATS score: {str(e)}")
