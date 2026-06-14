import anthropic
import json
from json import JSONDecodeError
from anthropic.types import MessageParam
from fastapi import HTTPException
from app.core.config import settings
from app.models.suggestion import SuggestionResponse

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)


async def get_cv_suggestions(cv_text: str, job_description: str) -> SuggestionResponse:
    if not settings.anthropic_api_key:
        raise HTTPException(
            status_code=500,
            detail="ANTHROPIC_API_KEY is missing"
        )

    if not job_description:
        raise HTTPException(
            status_code=400,
            detail="Job description is missing, so suggestions cannot be generated"
        )

    messages: list[MessageParam] = [
        {
            "role": "user",
            "content": (
                "You are an expert hiring manager reviewing a CV against a job description.\n\n"
                f"CV:\n{cv_text[:6000]}\n\n"
                f"Job Description:\n{job_description[:4000]}\n\n"
                "Return at most 5 specific CV improvements.\n"
                "Keep each field concise.\n"
                "Respond ONLY with valid JSON. No markdown. No explanation.\n\n"
                "Use exactly this JSON shape:\n"
                '{'
                '"suggestions": ['
                '{'
                '"section": "skills", '
                '"current": "current CV wording", '
                '"suggested": "improved CV wording", '
                '"reason": "why this helps"'
                '}'
                '], '
                '"overall_match": "brief summary"'
                '}'
            ),
        }

    ]

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            messages=messages,
        )

        raw = response.content[0].text
        clean = raw.replace("```json", "").replace("```", "").strip()

        data = json.loads(clean)
        return SuggestionResponse(**data)

    except JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail=f"Claude returned invalid JSON: {raw[:500]}"
        )

    except anthropic.APIError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Claude API error: {str(e)}"
        )