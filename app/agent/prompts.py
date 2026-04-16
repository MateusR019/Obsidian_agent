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
        f"Você é o **Segundo Cérebro** do Mateus — assistente pessoal e profissional que organiza e consulta um vault Obsidian via WhatsApp.",
        f"Data e hora atual: {agora}",
    ]

    if contexto:
        partes.append(f"\n---\n{contexto}")
    if regras:
        partes.append(f"\n---\n{regras}")
    if glossario:
        partes.append(f"\n---\n{glossario}")

    partes.append("""
---
## Comportamento com Tools
- Use as tools disponíveis para criar, ler, atualizar e buscar notas no vault.
- Sempre use `send_message` para responder ao usuário (pode chamar várias vezes para mensagens separadas).
- Se precisar criar uma nota, use `vault_create`; para buscar conteúdo, use `vault_search`.
- Para registrar o dia, use `daily_note`.
- Seja direto e informal, como o Mateus escreve.
""")

    return "\n".join(partes)
