"""Manual graph smoke test; safe to import during pytest collection."""
from src.graph import legal_graph


if __name__ == "__main__":
    print(legal_graph.invoke({"question": "My landlord has not returned my deposit."}))
