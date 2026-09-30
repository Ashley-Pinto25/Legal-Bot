from langchain_core.documents import Document

from src.citations import build_citations
from src.classifier import classify_legal_domains
from src.graph import legal_graph
from src.legal_analysis import understand_situation
from src.validator import validate_answer


def test_classifies_multiple_legal_domains():
    primary, secondary = classify_legal_domains("My employer withheld my salary and threatens termination.")
    assert primary == "Labour & Employment"
    assert "Contract Law" not in secondary  # no unsupported inferred domain


def test_situation_extraction_keeps_facts_separate_from_categories():
    result = understand_situation("My landlord retained ₹50,000 in Karnataka after I moved out.")
    assert result["primary_domain"] == "Property & Land"
    assert result["state"] == "Karnataka"
    assert result["facts"]["user_provided"]["amount"] == "₹50,000"
    assert result["facts"]["user_provided"]["question"].startswith("My landlord")


def test_graph_asks_for_state_before_property_research():
    result = legal_graph.invoke({"question": "My landlord refuses to return my security deposit."})
    assert "Which state or union territory" in result["answer"]
    assert result["citations"] == []


def test_follow_up_retains_prior_domain_and_updates_location():
    result = understand_situation("This occurred in Karnataka.", {"primary_domain": "Property & Land"})
    assert result["primary_domain"] == "Property & Land"
    assert result["state"] == "Karnataka"


def test_high_risk_empty_retrieval_still_has_safety_direction():
    result = legal_graph.invoke({"question": "I am in immediate danger because of a threat."})
    assert "immediate danger" in result["answer"].lower()


def test_citations_only_use_real_metadata():
    docs = [
        Document(page_content="Text", metadata={"title": "Consumer Protection Act, 2019", "section": "Section 35", "source_url": "https://example.gov.in", "source_name": "India Code", "status": "current"}),
        Document(page_content="Text", metadata={"title": "Missing source"}),
    ]
    citations = build_citations(docs)
    assert len(citations) == 1
    assert citations[0]["label"] == "Consumer Protection Act, 2019 — Section 35"


def test_validator_rejects_unverified_provisions_and_absolute_advice():
    citations = [{"provision": "Section 35", "title": "Act", "source_url": "https://example.gov.in", "source_name": "India Code", "status": "current", "label": "Act"}]
    assert not validate_answer("Section 420 definitely applies to you.", citations)[0]
    assert validate_answer("This may depend on the facts. Section 35 may be relevant.", citations)[0]
