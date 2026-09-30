"""Legal-only semantic retrieval with metadata and exact-reference boosting."""
from __future__ import annotations

import re
from typing import Any

from src.config import settings
from src.vectorstore import legal_collection_has_documents, load_vectorstore


def _is_current(metadata: dict[str, Any]) -> bool:
    return metadata.get("status", "unknown") == "current"


def retrieve_legal_sources(question: str, state: str | None = None, domain: str | None = None) -> list[Any]:
    if not legal_collection_has_documents():
        return []
    try:
        vectorstore = load_vectorstore()
        candidates = vectorstore.similarity_search(question, k=settings.top_k * 3)
    except Exception:
        return []
    exact = set(re.findall(r"\b(?:section|article)\s+\d+[a-zA-Z-]*\b", question, re.I))

    def score(document: Any) -> tuple[int, int, int]:
        metadata = document.metadata or {}
        provision = str(metadata.get("section") or metadata.get("article") or "").lower()
        return (
            1 if _is_current(metadata) else 0,
            1 if not state or metadata.get("state") in (None, "", state) else 0,
            1 if provision in {item.lower() for item in exact} else 0,
        )

    filtered = [doc for doc in candidates if _is_current(doc.metadata or {})]
    if not filtered:
        return []  # Unknown/repealed material must not silently become a current-law answer.
    return sorted(filtered, key=score, reverse=True)[: settings.top_k]


def get_retriever():
    """Compatibility helper for integrations expecting a LangChain retriever."""
    return load_vectorstore().as_retriever(search_kwargs={"k": settings.top_k})
