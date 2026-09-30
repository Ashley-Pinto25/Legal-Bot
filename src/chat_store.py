"""Small local-only SQLite store for browser-scoped legal research conversations."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from src.config import settings


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ConversationStore:
    def __init__(self, database_path: Path | None = None):
        self.database_path = database_path or settings.conversation_database
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY, profile_id TEXT NOT NULL, title TEXT NOT NULL,
                    context_json TEXT NOT NULL DEFAULT '{}', created_at TEXT NOT NULL, updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY, conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
                    role TEXT NOT NULL CHECK(role IN ('user', 'assistant')), content TEXT NOT NULL,
                    facts_json TEXT, created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS conversations_profile_updated ON conversations(profile_id, updated_at DESC);
                CREATE INDEX IF NOT EXISTS messages_conversation_created ON messages(conversation_id, created_at);
            """)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def list_conversations(self, profile_id: str) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute("SELECT id, title, updated_at FROM conversations WHERE profile_id = ? ORDER BY updated_at DESC", (profile_id,)).fetchall()
        return [dict(row) for row in rows]

    def create_conversation(self, profile_id: str, title: str = "New legal research") -> str:
        conversation_id, timestamp = str(uuid4()), _now()
        with self._connect() as connection:
            connection.execute("INSERT INTO conversations (id, profile_id, title, created_at, updated_at) VALUES (?, ?, ?, ?, ?)", (conversation_id, profile_id, title, timestamp, timestamp))
        return conversation_id

    def get_conversation(self, profile_id: str, conversation_id: str) -> dict | None:
        with self._connect() as connection:
            conversation = connection.execute("SELECT * FROM conversations WHERE id = ? AND profile_id = ?", (conversation_id, profile_id)).fetchone()
            if not conversation:
                return None
            messages = connection.execute("SELECT role, content, facts_json FROM messages WHERE conversation_id = ? ORDER BY created_at", (conversation_id,)).fetchall()
        payload = dict(conversation)
        payload["context"] = json.loads(payload.pop("context_json") or "{}")
        payload["messages"] = [{"role": row["role"], "content": row["content"], "facts": json.loads(row["facts_json"]) if row["facts_json"] else None} for row in messages]
        return payload

    def append_message(self, profile_id: str, conversation_id: str, role: str, content: str, facts: dict | None = None) -> None:
        timestamp = _now()
        with self._connect() as connection:
            if not connection.execute("SELECT 1 FROM conversations WHERE id = ? AND profile_id = ?", (conversation_id, profile_id)).fetchone():
                raise ValueError("Conversation is not available for this browser profile.")
            connection.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?)", (str(uuid4()), conversation_id, role, content, json.dumps(facts) if facts else None, timestamp))
            if role == "user":
                title = " ".join(content.split())[:72] or "New legal research"
                connection.execute("UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?", (title, timestamp, conversation_id))
            else:
                connection.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (timestamp, conversation_id))

    def update_context(self, profile_id: str, conversation_id: str, context: dict) -> None:
        with self._connect() as connection:
            connection.execute("UPDATE conversations SET context_json = ?, updated_at = ? WHERE id = ? AND profile_id = ?", (json.dumps(context), _now(), conversation_id, profile_id))
