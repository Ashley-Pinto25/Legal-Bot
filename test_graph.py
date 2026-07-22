from src.graph import graph

result = graph.invoke(
    {
        "question": "My salary is delayed."
    }
)

print(result)