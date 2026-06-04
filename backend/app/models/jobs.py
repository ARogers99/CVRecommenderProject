from pydantic import BaseModel

class Job(BaseModel):
    id: str
    title: str
    company: str
    location: str
    description: str
    url: str
    salary_min: float | None = None
    salary_max: float | None = None
    date_posted: str | None = None
    required_skills: list[str] = []