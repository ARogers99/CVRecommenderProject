from fastapi import APIRouter, HTTPException
from app.models.suggestion import SuggestionRequest, SuggestionResponse
from app.services.llm import get_cv_suggestions

router = APIRouter(prefix="/suggestions", tags=["suggestions"])

@router.post("/", response_model=SuggestionResponse)
async def get_suggestions(request: SuggestionRequest):
    try:
        suggestions = await get_cv_suggestions(
            cv_text=request.cv_text,
            job_description=request.job.description
        )
        return suggestions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get suggestions: {str(e)}")