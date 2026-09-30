"""Cached access to the dedicated legal Chroma collection.

The legacy default collection is intentionally left untouched. It contains the
former enterprise support corpus and must never be used as legal authority.
"""
from functools import lru_cache

import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from src.config import settings

LEGAL_COLLECTION = "indian_legal_sources"


def legal_collection_has_documents() -> bool:
    """Check collection state without loading an embedding model."""
    try:
        client = chromadb.PersistentClient(path=str(settings.chroma_persist_directory))
        return client.get_collection(LEGAL_COLLECTION).count() > 0
    except Exception:
        return False


@lru_cache(maxsize=1)
def get_embedding_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)


@lru_cache(maxsize=1)
def load_vectorstore() -> Chroma:
    return Chroma(
        collection_name=LEGAL_COLLECTION,
        persist_directory=str(settings.chroma_persist_directory),
        embedding_function=get_embedding_model(),
    )
