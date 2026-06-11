import anthropic
import json
from anthropic.types import MessageParam
from app.core.config import settings
from app.models.suggestion import SuggestionResponse

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)


async def get_cv_suggestions(cv_text: str, job_description: str) -> SuggestionResponse:
    messages: list[MessageParam] = [
        {
            "role": "user",
            "content":
                f"You are an expert hiring manager who reviews CVs for job placements.\n"
                f"Given the following CV and job description, suggest specific improvements to the CV to better match the job.\n\n"
                f"CV:\n{cv_text}\n\n"
                f"Job Description:\n{job_description}\n\n"
                f"Respond ONLY with a JSON object in exactly this format, no preamble or markdown:\n"
                f'{{"suggestions": [{{"section": "skills", "current": "what the cv currently says", '
                f'"suggested": "what to change it to", "reason": "why this change helps"}}], '
                f'"overall_match": "brief summary"}}'
        }
    ]
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=messages
    )
    raw = response.content[0].text
    clean = raw.replace("```json", "").replace("```", "").strip()
    data = json.loads(clean)
    return SuggestionResponse(**data)