from pydantic import BaseModel, Field
from typing import Optional

class CVData(BaseModel):
    raw_text: str
    name: Optional[str] = None
    email: Optional[str] = None
    skills: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)