from pydantic import BaseModel
from typing import Optional


class Job(BaseModel):
    job_id: Optional[str] = None
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    salary: Optional[str] = None
    source: Optional[str] = None