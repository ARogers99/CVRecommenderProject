from pydantic import BaseModel
from app.models.jobs import Job

class JobMatch(BaseModel):
    job: Job
    score: float
    matching_skills: list[str] = []
    missing_skills: list[str] = []

class MatchResponse(BaseModel):
    matches: list[JobMatch]
    total: int = 0