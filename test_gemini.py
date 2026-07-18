from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

response = client.models.generate_content(
    model=os.getenv("GEMINI_MODEL"),
    contents="Hello!"
)

print(response.text)