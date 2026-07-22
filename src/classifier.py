from src.gemini import generate_response
from src.prompts import CLASSIFIER_PROMPT


def classify_department(question: str) -> str:
    """
    Classifies a user's question into a department.
    """

    prompt = CLASSIFIER_PROMPT.format(
        question=question
    )

    department = generate_response(prompt).strip()

    return department