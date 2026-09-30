"""Manual classifier explorer; safe to import during pytest collection."""
from src.classifier import classify_legal_domains


if __name__ == "__main__":
    while True:
        question = input("\nDescribe a legal situation (or 'exit'): ").strip()
        if question.lower() == "exit":
            break
        print(classify_legal_domains(question))
