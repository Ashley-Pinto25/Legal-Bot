"""Small, lazy Gemini adapter with safe failure modes."""
from functools import lru_cache

from src.config import settings


class GeminiUnavailable(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client():
    if not settings.google_api_key:
        raise GeminiUnavailable("Gemini is not configured. Set GOOGLE_API_KEY to enable synthesis.")
    try:
        from google import genai
        return genai.Client(api_key=settings.google_api_key)
    except Exception as exc:
        raise GeminiUnavailable("Gemini client could not be initialized.") from exc


def generate_response(prompt: str) -> str:
    try:
        response = get_client().models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config={"temperature": settings.temperature},
        )
        text = getattr(response, "text", None)
        if not text:
            raise GeminiUnavailable("Gemini returned an empty response.")
        return text
    except GeminiUnavailable:
        raise
    except Exception as exc:
        raise GeminiUnavailable("Gemini is temporarily unavailable. Please try again later.") from exc
