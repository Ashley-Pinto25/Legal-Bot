"""Central configuration for the Indian Legal Assistant.

No credentials are stored in this repository. Paths are resolved from this
package so the app behaves the same whether it is launched from its root or by
a process manager.
"""
from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def _embedding_model() -> str:
    configured = os.getenv("EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)
    # Gemini's `models/...` identifiers are API embedding models, not
    # HuggingFace model identifiers. Chroma's local HuggingFace adapter cannot
    # load them; use the documented project default rather than retrying a
    # network request for a non-existent HuggingFace repository.
    return DEFAULT_EMBEDDING_MODEL if configured == "models/gemini-embedding-2" else configured


@dataclass(frozen=True)
class Settings:
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    embedding_model: str = _embedding_model()
    chroma_persist_directory: Path = Path(os.getenv("CHROMA_PERSIST_DIRECTORY", str(BASE_DIR / "vectorstores")))
    legal_knowledge_directory: Path = Path(os.getenv("LEGAL_KNOWLEDGE_DIRECTORY", str(BASE_DIR / "knowledge" / "legal")))
    conversation_database: Path = Path(os.getenv("CONVERSATION_DATABASE", str(BASE_DIR / "data" / "conversations.db")))
    top_k: int = int(os.getenv("TOP_K", "5"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1200"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "150"))
    temperature: float = float(os.getenv("TEMPERATURE", "0"))


settings = Settings()
GOOGLE_API_KEY = settings.google_api_key
MODEL = settings.gemini_model
EMBEDDING_MODEL = settings.embedding_model
