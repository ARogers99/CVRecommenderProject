from fastapi import APIRouter, HTTPException, Request

from app.core.limiter import limiter
from app.models.suggestion import SuggestionRequest, SuggestionResponse
from app.services.llm import get_cv_suggestions

router = APIRouter(prefix="/suggestions", tags=["suggestions"])


@router.post("/", response_model=SuggestionResponse)
@limiter.limit("3/hour")
async def get_suggestions(request: Request, body: SuggestionRequest):
    try:
        return await get_cv_suggestions(
            cv_text=body.cv_text,
            job_description=body.job.description or "",
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get suggestions: {repr(e)}",
        )