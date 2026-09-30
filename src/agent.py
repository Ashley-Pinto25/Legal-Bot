"""Public legal-answer entry point used by the Streamlit UI."""
from __future__ import annotations

from typing import Any

from src.graph import legal_graph
from src.state import LEGAL_DISCLAIMER


def ask(question: str, history: list[dict[str, str]] | None = None, legal_context: dict[str, Any] | None = None) -> dict[str, Any]:
    result = legal_graph.invoke(
        {"question": question, "conversation_history": history or [], "prior_context": legal_context or {}}
    )
    result["answer"] = result.get("answer", "I could not verify this from the available legal sources.")
    result["disclaimer"] = LEGAL_DISCLAIMER
    return result
