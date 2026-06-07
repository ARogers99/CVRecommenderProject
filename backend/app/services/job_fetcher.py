import httpx
from app.models.jobs import Job
from app.core.config import settings

ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs"


async def fetch_jobs(keywords: str, location: str = "ireland", results: int = 10) -> list[Job]:
    url = f"{ADZUNA_BASE_URL}/gb/search/1"

    params = {
        "app_id": settings.adzuna_app_id,
        "app_key": settings.adzuna_app_key,
        "results_per_page": results,
        "what": keywords,
        "where": location,
        "content-type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    jobs = []
    for result in data.get("results", []):
        job = Job(
            id=str(result.get("id", "")),
            title=result.get("title", ""),
            company=result.get("company", {}).get("display_name", ""),
            location=result.get("location", {}).get("display_name", ""),
            description=result.get("description", ""),
            url=result.get("redirect_url", ""),
            salary_min=result.get("salary_min"),
            salary_max=result.get("salary_max"),
            date_posted=result.get("created"),
        )
        jobs.append(job)

    return jobs