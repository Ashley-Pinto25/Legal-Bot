from typing import Any, TypedDict

import streamlit as st

LEGAL_DISCLAIMER = (
    "This assistant provides general legal information based on available sources. "
    "It does not provide legal representation or replace advice from a qualified "
    "advocate. Laws and procedures may change, and applicability depends on the facts "
    "and jurisdiction."
)


def initialize_session() -> None:
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("legal_context", {})


class LegalGraphState(TypedDict, total=False):
    question: str
    conversation_history: list[dict[str, str]]
    prior_context: dict[str, Any]
    issue_summary: str
    legal_domains: list[str]
    primary_domain: str
    secondary_domains: list[str]
    jurisdiction: str
    state: str | None
    facts: dict[str, Any]
    missing_information: list[str]
    clarification_question: str | None
    documents: list[Any]
    context: str
    citations: list[dict[str, Any]]
    answer: str
    risk_level: str
    error: str


# Existing callers can continue importing GraphState.
GraphState = LegalGraphState
