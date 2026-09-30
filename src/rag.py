"""Structure-aware legal ingestion. Run: python scripts/ingest.py.

Only documents placed beneath knowledge/legal with a matching metadata sidecar
are ingested. This protects the legal collection from the old enterprise PDFs
and refuses to fabricate source or version information.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import settings
from src.vectorstore import load_vectorstore

REQUIRED_METADATA = {"title", "source_type", "source_url", "official_source", "status", "jurisdiction"}
SECTION_PATTERN = re.compile(r"(?im)^\s*((?:section|article)\s+\d+[a-zA-Z-]*)\.?\s*")


def _metadata_for(pdf_path: Path) -> dict | None:
    sidecar = pdf_path.with_suffix(".metadata.json")
    if not sidecar.exists():
        return None
    metadata = json.loads(sidecar.read_text(encoding="utf-8"))
    missing = REQUIRED_METADATA - metadata.keys()
    if missing:
        raise ValueError(f"{sidecar}: missing required metadata: {', '.join(sorted(missing))}")
    return metadata


def structure_aware_chunks(documents: list[Document], metadata: dict) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)
    chunks: list[Document] = []
    for document in documents:
        text = document.page_content
        parts = SECTION_PATTERN.split(text)
        # Pair a detected section heading with its following content. If the PDF
        # has no parseable heading, retain page boundaries rather than guessing.
        groups = [text] if len(parts) == 1 else ["".join(parts[index:index + 2]) for index in range(1, len(parts), 2)]
        for group in groups:
            section_match = SECTION_PATTERN.search(group)
            section = section_match.group(1) if section_match else metadata.get("section")
            for chunk in splitter.split_text(group):
                chunk_metadata = {**metadata, **document.metadata, "section": section}
                chunks.append(Document(page_content=chunk, metadata=chunk_metadata))
    return chunks


def ingest_legal_documents() -> int:
    root = settings.legal_knowledge_directory
    if not root.exists():
        return 0
    chunks: list[Document] = []
    for pdf_path in root.rglob("*.pdf"):
        metadata = _metadata_for(pdf_path)
        if metadata is None:
            continue
        if metadata["status"] != "current":
            # A text that is only partially commenced, historical, repealed or
            # otherwise unverified must not enter the current-law collection.
            continue
        pages = PyPDFLoader(str(pdf_path)).load()
        chunks.extend(structure_aware_chunks(pages, metadata))
    if chunks:
        load_vectorstore().add_documents(chunks)
    return len(chunks)
