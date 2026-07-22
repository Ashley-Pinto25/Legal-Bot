from src.classifier import classify_department

while True:

    question = input("\nQuestion: ")

    if question.lower() == "exit":
        break

    department = classify_department(question)

    print(f"\nDepartment: {department}")