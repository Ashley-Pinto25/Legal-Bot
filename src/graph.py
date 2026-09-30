"""LangGraph workflow for cautious, source-grounded Indian legal information."""
from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from src.citations import build_citations, format_citations
from src.gemini import GeminiUnavailable, generate_response
from src.legal_analysis import clarification_question, understand_situation
from src.prompts import RAG_PROMPT
from src.retriever import retrieve_legal_sources
from src.state import LegalGraphState
from src.validator import validate_answer


def understand_situation_node(state: LegalGraphState):
    analysis = understand_situation(state["question"], state.get("prior_context", {}))
    return analysis


def check_missing_information_node(state: LegalGraphState):
    question = clarification_question(state)
    if question:
        return {"clarification_question": question}
    return {}


def route_after_missing_information(state: LegalGraphState) -> str:
    return "clarification_required" if state.get("clarification_question") and state.get("risk_level") != "high" else "retrieve_legal_sources"


def clarification_required_node(state: LegalGraphState):
    return {
        "answer": (
            "To narrow the legal research accurately, I need one detail first: "
            f"{state['clarification_question']}\n\n"
            "I have not assumed a state or any other fact that you did not provide."
        ),
        "documents": [],
        "citations": [],
    }


def retrieve_legal_sources_node(state: LegalGraphState):
    docs = retrieve_legal_sources(state["question"], state.get("state"), state.get("primary_domain"))
    return {"documents": docs}


def build_context_node(state: LegalGraphState):
    context = []
    for document in state.get("documents", []):
        metadata = document.metadata or {}
        context.append(
            f"TITLE: {metadata.get('title', 'Unknown')}\n"
            f"PROVISION: {metadata.get('section') or metadata.get('article') or 'Not specified'}\n"
            f"STATUS: {metadata.get('status', 'unknown')}\n"
            f"TEXT:\n{document.page_content}"
        )
    return {"context": "\n\n---\n\n".join(context), "citations": build_citations(state.get("documents", []))}


def generate_answer_node(state: LegalGraphState):
    prefix = ""
    if state.get("risk_level") == "high":
        prefix = (
            "Because this may involve a serious or urgent matter, consider contacting the relevant "
            "authority, legal aid service, or a qualified advocate promptly. If you are in immediate "
            "danger, contact emergency services.\n\n"
        )
    if not state.get("documents"):
        return {"answer": prefix + "I could not verify this from the available legal sources. The current legal collection may not cover this issue yet."}
    try:
        answer = generate_response(RAG_PROMPT.format(context=state["context"], question=state["question"]))
    except GeminiUnavailable as exc:
        answer = (
            "Relevant source material was retrieved, but a grounded summary is unavailable because "
            f"{exc} You can review the verified source links below."
        )
    return {"answer": prefix + answer}


def validate_answer_node(state: LegalGraphState):
    # Emergency-oriented wording is safety information, not an asserted legal
    # proposition, and must remain visible even when no legal source is indexed.
    if state.get("risk_level") == "high" and not state.get("citations"):
        return {"error": None}
    valid, answer = validate_answer(state.get("answer", ""), state.get("citations", []))
    return {"answer": answer, "error": None if valid else "Answer validation returned a safer response."}


def format_citations_node(state: LegalGraphState):
    sources = format_citations(state.get("citations", []))
    return {"answer": state["answer"] + ("\n\n" + sources if sources else "")}


workflow = StateGraph(LegalGraphState)
workflow.add_node("understand_situation", understand_situation_node)
workflow.add_node("check_missing_information", check_missing_information_node)
workflow.add_node("clarification_required", clarification_required_node)
workflow.add_node("retrieve_legal_sources", retrieve_legal_sources_node)
workflow.add_node("build_context", build_context_node)
workflow.add_node("generate_answer", generate_answer_node)
workflow.add_node("validate_answer", validate_answer_node)
workflow.add_node("format_citations", format_citations_node)
workflow.add_edge(START, "understand_situation")
workflow.add_edge("understand_situation", "check_missing_information")
workflow.add_conditional_edges("check_missing_information", route_after_missing_information)
workflow.add_edge("clarification_required", END)
workflow.add_edge("retrieve_legal_sources", "build_context")
workflow.add_edge("build_context", "generate_answer")
workflow.add_edge("generate_answer", "validate_answer")
workflow.add_edge("validate_answer", "format_citations")
workflow.add_edge("format_citations", END)
legal_graph = workflow.compile()
graph = legal_graph
