from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.match import MatchResponse
from app.services.job_fetcher import fetch_jobs
from app.services.matcher import match_cv_job

router = APIRouter(prefix="/match", tags=["match"])


class MatchRequest(BaseModel):
    keywords: str
    location: str
    cv_text: str
    num_pages: int = 1


@router.post("/", response_model=MatchResponse)
async def job_match(request: MatchRequest):
    try:
        jobs = await fetch_jobs(request.keywords,request.location,request.num_pages,)

        return match_cv_job(request.cv_text, jobs)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Matching failed: {repr(e)}")