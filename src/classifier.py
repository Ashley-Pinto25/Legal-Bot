"""Conservative, explainable legal-domain classification."""
from __future__ import annotations

from collections import OrderedDict

DOMAIN_PATTERNS: "OrderedDict[str, tuple[str, ...]]" = OrderedDict(
    {
        "Criminal Law": ("fir", "arrest", "police", "bail", "crime", "threat", "assault", "bns", "bnss"),
        "Family Law": ("husband", "wife", "marriage", "divorce", "maintenance", "domestic violence", "child custody"),
        "Labour & Employment": ("salary", "wage", "employer", "employee", "termination", "workplace", "gratuity"),
        "Consumer Protection": ("defective", "refund", "consumer", "seller", "product", "service complaint"),
        "Property & Land": ("landlord", "tenant", "rent", "deposit", "property", "lease", "land"),
        "Cyber Law": ("online", "cyber", "photograph", "photo", "privacy", "data", "social media", "internet"),
        "Banking & Financial": ("bank", "loan", "upi", "fraud", "insurance", "credit card"),
        "Motor Vehicles": ("accident", "vehicle", "driving", "traffic", "motor"),
        "Constitutional Rights": ("constitution", "article", "fundamental right", "writ"),
        "Contract Law": ("contract", "agreement", "breach", "notice"),
        "Intellectual Property": ("copyright", "trademark", "patent"),
        "Environmental Law": ("pollution", "noise", "environment"),
        "Education": ("school", "college", "university", "admission"),
        "Immigration / Citizenship": ("citizenship", "visa", "passport", "immigration"),
        "Taxation": ("tax", "gst", "income tax"),
        "Government Schemes / Legal Services": ("legal aid", "nalsa", "government scheme", "lok adalat"),
    }
)


def classify_legal_domains(question: str) -> tuple[str, list[str]]:
    text = question.lower()
    ranked = [
        (domain, sum(term in text for term in terms), index)
        for index, (domain, terms) in enumerate(DOMAIN_PATTERNS.items())
    ]
    matches = sorted((item for item in ranked if item[1]), key=lambda item: (-item[1], item[2]))
    domains = [domain for domain, _score, _index in matches]
    return (domains[0], domains[1:]) if domains else ("General / Multiple Domains", [])


def classify_department(question: str) -> str:
    """Compatibility wrapper for callers of the pre-legal classifier."""
    return classify_legal_domains(question)[0]
