from pydantic import BaseModel
from app.models.jobs import Job


class SuggestionRequest(BaseModel):
    cv_text: str
    job: Job

class Suggestion(BaseModel):
    section: str
    current: str        # what the CV currently says
    suggested: str      # what the LLM recommends instead
    reason: str         # why this change helps

class SuggestionResponse(BaseModel):
    suggestions: list[Suggestion]
    overall_match: str