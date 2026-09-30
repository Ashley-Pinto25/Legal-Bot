"""Situation extraction and jurisdiction detection without inventing facts."""
from __future__ import annotations

import re
from typing import Any

from src.classifier import classify_legal_domains

INDIAN_STATES = (
    "andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh", "goa",
    "gujarat", "haryana", "himachal pradesh", "jharkhand", "karnataka", "kerala",
    "madhya pradesh", "maharashtra", "manipur", "meghalaya", "mizoram", "nagaland",
    "odisha", "punjab", "rajasthan", "sikkim", "tamil nadu", "telangana", "tripura",
    "uttar pradesh", "uttarakhand", "west bengal", "delhi",
)
HIGH_RISK_TERMS = (
    "arrest", "custody", "domestic violence", "sexual", "child abuse", "immediate danger",
    "threat", "suicide", "serious injury", "police notice", "summons",
)


def _find_state(text: str) -> str | None:
    lowered = text.lower()
    return next((state.title() for state in INDIAN_STATES if state in lowered), None)


def understand_situation(question: str, prior_context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return only values supported by the question or explicitly retained context."""
    prior_context = prior_context or {}
    primary, secondary = classify_legal_domains(question)
    if primary == "General / Multiple Domains" and prior_context.get("primary_domain"):
        # A short follow-up such as "This was in Karnataka" belongs to the
        # already identified situation; the legal category is retained, not
        # invented anew from the follow-up text.
        primary = str(prior_context["primary_domain"])
    lowered = question.lower()
    state = _find_state(question) or prior_context.get("state")
    amount = re.search(r"(?:₹|rs\.?|inr\s*)\s?([\d,]+)", question, re.I)
    facts: dict[str, Any] = {"user_provided": {"question": question}}
    if amount:
        facts["user_provided"]["amount"] = amount.group(0)
    if state and _find_state(question):
        facts["user_provided"]["state"] = state

    missing: list[str] = []
    needs_location = primary in {"Property & Land", "Family Law", "Labour & Employment", "Environmental Law"}
    if needs_location and not state:
        missing.append("state or union territory")
    if primary in {"Property & Land", "Contract Law"} and "agreement" not in lowered:
        missing.append("whether there is a written agreement and its relevant terms")
    if primary == "Labour & Employment" and not any(word in lowered for word in ("employee", "contractor", "appointment")):
        missing.append("whether you are an employee or an independent contractor")

    risk = "high" if any(term in lowered for term in HIGH_RISK_TERMS) else "normal"
    return {
        "issue_summary": question.strip(),
        "primary_domain": primary,
        "secondary_domains": secondary,
        "legal_domains": [primary, *secondary],
        "state": state,
        "jurisdiction": f"India — {state}" if state else "India (state/local jurisdiction not specified)",
        "facts": facts,
        "missing_information": missing,
        "risk_level": risk,
    }


def clarification_question(analysis: dict[str, Any]) -> str | None:
    if "state or union territory" in analysis.get("missing_information", []):
        return "Which state or union territory did this occur in? State and local rules or the relevant forum may matter."
    return None
