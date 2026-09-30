"""Manual smoke test; safe to import during pytest collection."""
from src.agent import ask


if __name__ == "__main__":
    while True:
        question = input("\nDescribe a legal situation (or 'exit'): ").strip()
        if question.lower() == "exit":
            break
        print("\nAnswer:\n", ask(question)["answer"])
