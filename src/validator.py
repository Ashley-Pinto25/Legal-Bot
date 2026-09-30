"""Guardrails for a source-grounded legal information answer."""
from __future__ import annotations

import re

UNSAFE_PATTERNS = ("you definitely have a case", "you will win", "you should sue", "definitely applies")


def validate_answer(answer: str, citations: list[dict[str, str]]) -> tuple[bool, str]:
    if not citations:
        return False, "I could not verify this from the available legal sources."
    lowered = answer.lower()
    if any(pattern in lowered for pattern in UNSAFE_PATTERNS):
        return False, "I could not safely verify a personalized legal conclusion from the available legal sources."
    allowed_provisions = {citation["provision"].lower() for citation in citations if citation.get("provision")}
    mentioned = {match.lower() for match in re.findall(r"\b(?:section|article)\s+\d+[a-zA-Z-]*", answer, re.I)}
    if mentioned and not mentioned.issubset(allowed_provisions):
        return False, "I could not verify every legal provision in a generated answer from the retrieved sources."
    if "may" not in lowered and "depends" not in lowered and "can" not in lowered:
        answer = "Based on the available source material, the following information may be relevant.\n\n" + answer
    return True, answer
