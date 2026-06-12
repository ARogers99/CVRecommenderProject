from fastapi import APIRouter, HTTPException, Query
from app.models.jobs import Job
from app.services.job_fetcher import fetch_jobs

router = APIRouter(prefix="/jobs", tags=["jobs"])


VALID_COUNTRIES = {
    "gb": "United Kingdom",
    "us": "United States",
    "ca": "Canada",
    "au": "Australia",
    "de": "Germany",
    "fr": "France",
    "nl": "Netherlands",
}

@router.get("/", response_model=list[Job])
async def get_jobs(
    query: str = Query(..., description="Job search keywords eg. Python Developer"),
    location: str = Query(default="gb", description="Location to search in"),
    num_pages: int = Query(default=1, description="Number of pages to fetch"),
):

    if location not in VALID_COUNTRIES:
        raise HTTPException(status_code=400, detail="Invalid country code")
    try:
        jobs = await fetch_jobs(query, location,num_pages)
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch jobs: {str(e)}")

@router.get("/countries")
async def get_countries():
    return [
        {"name": name, "code": code}
        for code, name in VALID_COUNTRIES.items()
    ]