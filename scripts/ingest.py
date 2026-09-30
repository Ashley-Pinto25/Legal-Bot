"""Ingest validated official legal PDFs into the dedicated Chroma collection."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.rag import ingest_legal_documents  # noqa: E402


if __name__ == "__main__":
    count = ingest_legal_documents()
    print(f"Ingested {count} legal chunks.")
