"""Histórico de conversas por sessão, persistido no SQLite."""
import json
from datetime import datetime
from app.db.connection import get_connection
from app.providers.llm.base import Message
from app.utils.logger import get_logger

logger = get_logger(__name__)


def ensure_session(session_id: str, phone: str) -> None:
    conn = get_connection()
    conn.execute("""
        INSERT INTO sessions (id, phone, last_seen) VALUES (?, ?, datetime('now'))
        ON CONFLICT(id) DO UPDATE SET last_seen=datetime('now')
    """, (session_id, phone))
    conn.commit()


def save_message(
    session_id: str,
    role: str,
    content: str,
    message_id: str | None = None,
    tool_name: str | None = None,
    tool_call_id: str | None = None,
) -> None:
    conn = get_connection()
    conn.execute("""
        INSERT OR IGNORE INTO messages (session_id, message_id, role, content, tool_name, tool_call_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (session_id, message_id, role, content, tool_name, tool_call_id))
    conn.commit()


def get_history(session_id: str, window: int = 20) -> list[Message]:
    conn = get_connection()
    rows = conn.execute("""
        SELECT role, content, tool_name, tool_call_id
        FROM messages
        WHERE session_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (session_id, window)).fetchall()

    messages: list[Message] = []
    for row in reversed(rows):
        content = row["content"]
        # Tenta desserializar conteúdo multimodal salvo como JSON
        try:
            parsed = json.loads(content)
            if isinstance(parsed, list):
                content = parsed
        except (json.JSONDecodeError, TypeError):
            pass

        messages.append(Message(
            role=row["role"],
            content=content,
            tool_call_id=row["tool_call_id"],
        ))
    return messages


def is_duplicate(message_id: str) -> bool:
    conn = get_connection()
    row = conn.execute("SELECT 1 FROM messages WHERE message_id=?", (message_id,)).fetchone()
    return row is not None
