"""Tool para enviar mensagem de volta ao usuário via Evolution API."""
import httpx
from app.tools.registry import tool
from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Session phone é injetado pelo orchestrator antes de cada chamada
_current_phone: str = ""


def set_current_phone(phone: str) -> None:
    global _current_phone
    _current_phone = phone


@tool(
    name="send_message",
    description="Envia uma mensagem de texto para o usuário via WhatsApp.",
    schema={
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "Texto da mensagem a enviar"},
        },
        "required": ["text"],
    },
)
def send_message(text: str) -> dict:
    settings = get_settings()
    phone = _current_phone

    if not phone:
        logger.warning("send_message chamada sem phone configurado")
        return {"ok": False, "error": "Destinatário não configurado"}

    url = f"{settings.evolution_url}/message/sendText/{settings.evolution_instance}"
    payload = {
        "number": phone,
        "text": text,
    }
    headers = {"apikey": settings.evolution_api_key}

    try:
        resp = httpx.post(url, json=payload, headers=headers, timeout=15)
        resp.raise_for_status()
        logger.info(f"Mensagem enviada para {phone}: {text[:50]!r}")
        return {"ok": True}
    except Exception as e:
        logger.error(f"Falha ao enviar mensagem para {phone}: {e}")
        return {"ok": False, "error": str(e)}
