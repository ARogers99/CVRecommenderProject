import anthropic
from app.core.config import settings
from app.models.suggestion import SuggestionResponse

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)


async def get_cv_suggestions(cv_text: str, job_description: str) -> SuggestionResponse:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[]
    )
    return SuggestionResponse.model_validate_json(response.content[0].text)