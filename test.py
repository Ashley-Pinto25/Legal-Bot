from src.agent import ask

while True:

    question = input("\nAsk a question: ")

    if question.lower() == "exit":
        break

    answer = ask(question)

    print("\nAnswer:\n")
    print(answer)