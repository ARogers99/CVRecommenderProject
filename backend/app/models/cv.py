from pydantic import BaseModel

class CVData(BaseModel):
    raw_text: str
    name: str | None = None
    email: str | None = None
    skills: list[str] = []
    experience: list[str] = []
    education: list[str] = []