from google import genai

from src.config import GOOGLE_API_KEY
from src.config import MODEL

client = genai.Client(api_key=GOOGLE_API_KEY)


def ask_gemini(prompt):

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text