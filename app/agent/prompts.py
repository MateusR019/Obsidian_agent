"""Constrói o system prompt do agente dinamicamente."""
from datetime import datetime
from pathlib import Path
from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _read_system_file(filename: str) -> str:
    settings = get_settings()
    path = Path(settings.vault_path) / "_SYSTEM" / filename
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""


def build_system_prompt() -> str:
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    regras = _read_system_file("regras.md")
    glossario = _read_system_file("glossario.md")
    contexto = _read_system_file("contexto_negocio.md")

    partes = [
        "You are the user's **Second Brain** — a personal AI assistant that organizes "
        "and retrieves knowledge from an Obsidian vault via WhatsApp.",
        f"Current date and time: {agora}",
    ]

    if contexto:
        partes.append(f"\n---\n{contexto}")
    if regras:
        partes.append(f"\n---\n{regras}")
    if glossario:
        partes.append(f"\n---\n{glossario}")

    partes.append("""
---
## Tool Behavior
- Use available tools to create, read, update and search notes in the vault.
- Always use `send_message` to reply to the user (can call multiple times for separate messages).
- For creating notes use `vault_create`; for searching use `vault_search`.
- For the day's log use `daily_note`.
- Be concise and direct.
""")

    return "\n".join(partes)
