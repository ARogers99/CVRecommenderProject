from fastapi import APIRouter, HTTPException, Query
from app.models.jobs import Job
from app.services.job_fetcher import fetch_jobs

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/", response_model=list[Job])
async def get_jobs(
    keywords: str = Query(..., description="Job search keywords eg. Python Developer"),
    location: str = Query(default="ireland", description="Location to search in"),
    results: int = Query(default=10, ge=1, le=50)
):
    try:
        jobs = await fetch_jobs(keywords, location, results)
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch jobs: {str(e)}")