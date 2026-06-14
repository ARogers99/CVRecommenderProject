from fastapi import APIRouter, HTTPException, Request
from app.models.suggestion import SuggestionRequest, SuggestionResponse
from app.services.llm import get_cv_suggestions
from app.main import limiter

router = APIRouter(prefix="/suggestions", tags=["suggestions"])


@router.post("/", response_model=SuggestionResponse)
@limiter.limit("5/hour")
async def get_suggestions(request:Request, body: SuggestionRequest):
    try:
        return await get_cv_suggestions(
            cv_text=request.cv_text,
            job_description=request.job.description or ""
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get suggestions: {repr(e)}"
        )