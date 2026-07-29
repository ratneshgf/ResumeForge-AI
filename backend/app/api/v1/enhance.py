import logging
from fastapi import APIRouter, Depends, HTTPException

from app.core import session_store
from app.core.rate_limit import rate_limit
from app.schemas.enhancement import EnhanceRequest, EnhanceResponse
from app.services.ai_engine.resume_enhancer import enhance_resume
from app.services.ai_engine.client import AIClientError

router = APIRouter(prefix="/api/v1/enhance", tags=["enhance"])
logger = logging.getLogger(__name__)


@router.post("/full", response_model=EnhanceResponse, dependencies=[Depends(rate_limit)])
async def enhance_full(payload: EnhanceRequest):
    data = session_store.get(payload.session_id)
    if "sections" not in data:
        raise HTTPException(404, "Upload and parse a resume for this session first")

    try:
        logger.info(f"Starting resume enhancement for session {payload.session_id}")
        changes = enhance_resume(data["sections"], payload.job_description)
        
        session_store.set_value(payload.session_id, "changes", changes)
        session_store.set_value(payload.session_id, "job_description", payload.job_description)
        
        logger.info(f"Enhancement complete: {len(changes)} changes generated")
        
        return EnhanceResponse(
            session_id=payload.session_id,
            resume_id=payload.resume_id,
            changes=changes,
        )
    
    except AIClientError as e:
        logger.error(f"AI enhancement failed: {e}")
        raise HTTPException(
            503,
            f"AI service error: {str(e)}. Please check your API configuration and try again."
        )
    
    except Exception as e:
        logger.error(f"Enhancement error: {e}", exc_info=True)
        raise HTTPException(500, f"Error enhancing resume: {str(e)}")
