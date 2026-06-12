import httpx
from fastapi import HTTPException
from app.models.jobs import Job
from app.core.config import settings

JSEARCH_BASE_URL = "https://api.openwebninja.com/jsearch/search-v2"
JSEARCH_API_KEY = settings.jsearch_api_key


async def fetch_jobs(query: str, location: str, num_pages: int) -> list[Job]:
    params_jsearch = {
        "query": query,
        "country": location,
        "language": "en",
        "num_pages": num_pages,
    }
    jsearch_headers = {
        "x-api-key" : JSEARCH_API_KEY
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(JSEARCH_BASE_URL, headers=jsearch_headers, params=params_jsearch)
            response.raise_for_status()
            data = response.json()

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code,detail=e.response.text)

    except httpx.RequestError as e:
        raise HTTPException(status_code=502,detail=f"Failed to connect to JSearch API: {repr(e)}")


    jobs = []
    for result in data.get("data", {}).get("jobs", []):
        job = Job(
            job_id=result.get("job_id"),
            title=result.get("job_title", "Unknown title"),
            company=result.get("employer_name"),
            location=result.get("job_location"),
            description=result.get("job_description") or "",
            link=result.get("job_apply_link"),
            salary=result.get("job_salary"),
            source=result.get("job_publisher"),
        )
        jobs.append(job)
    return jobs