"""Download e transcrição de áudio via STT provider."""
import httpx
from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


def download_media(instance: str, message_id: str, api_key: str) -> bytes:
    """Baixa mídia da Evolution API pelo message_id."""
    settings = get_settings()
    url = f"{settings.evolution_url}/chat/getBase64FromMediaMessage/{instance}"
    resp = httpx.post(
        url,
        json={"key": {"id": message_id}},
        headers={"apikey": api_key},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    import base64
    b64 = data.get("base64", "")
    return base64.b64decode(b64)


def transcribe_audio(message_id: str) -> str:
    """Baixa áudio e transcreve via STT provider configurado."""
    settings = get_settings()
    try:
        audio_bytes = download_media(settings.evolution_instance, message_id, settings.evolution_api_key)
    except Exception as e:
        logger.error(f"Falha ao baixar áudio {message_id}: {e}")
        return "[áudio não disponível]"

    from app.providers.stt.factory import get_stt
    stt = get_stt()
    try:
        text = stt.transcribe(audio_bytes, mime_type="audio/ogg")
        logger.info(f"Áudio transcrito: {text[:80]!r}")
        return text
    except Exception as e:
        logger.error(f"STT falhou para {message_id}: {e}")
        return "[não consegui transcrever o áudio]"
