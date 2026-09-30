"""Deterministic citations built solely from retrieved document metadata."""
from __future__ import annotations

from pathlib import Path
from typing import Any


def build_citations(documents: list[Any]) -> list[dict[str, str]]:
    citations: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for document in documents:
        metadata = getattr(document, "metadata", {}) or {}
        title = metadata.get("title") or metadata.get("act_name")
        source_url = metadata.get("source_url") or metadata.get("official_source")
        if not title or not source_url:
            # There is no safe, displayable citation when required metadata is absent.
            continue
        provision = metadata.get("section") or metadata.get("article") or ""
        page = metadata.get("page")
        label = f"{title}{' — ' + str(provision) if provision else ''}"
        if page is not None:
            label += f" — Pg. {int(page) + 1}"
        identity = (str(title), str(provision), str(source_url))
        if identity in seen:
            continue
        seen.add(identity)
        citations.append(
            {
                "label": label,
                "title": str(title),
                "provision": str(provision),
                "source_name": str(metadata.get("source_name", "Official source")),
                "source_url": str(source_url),
                "status": str(metadata.get("status", "unknown")),
            }
        )
    return citations


def format_citations(citations: list[dict[str, str]]) -> str:
    if not citations:
        return ""
    lines = ["## Sources"]
    for citation in citations:
        status = "" if citation["status"] == "current" else f" (status: {citation['status']})"
        lines.append(f"- [{citation['label']}]({citation['source_url']}) — {citation['source_name']}{status}")
    return "\n".join(lines)
