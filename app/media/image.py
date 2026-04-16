"""Download e preparação de imagens para LLM vision."""
import base64
import httpx
from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


def get_image_content(message_id: str, mime_type: str = "image/jpeg") -> list[dict]:
    """
    Baixa imagem e retorna content multimodal para LLM vision.
    Formato compatível com Gemini e OpenAI vision.
    """
    settings = get_settings()
    try:
        url = f"{settings.evolution_url}/chat/getBase64FromMediaMessage/{settings.evolution_instance}"
        resp = httpx.post(
            url,
            json={"key": {"id": message_id}},
            headers={"apikey": settings.evolution_api_key},
            timeout=30,
        )
        resp.raise_for_status()
        b64 = resp.json().get("base64", "")
        logger.info(f"Imagem baixada para {message_id}")
        return [
            {"type": "text", "text": "Analise esta imagem:"},
            {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{b64}"}},
        ]
    except Exception as e:
        logger.error(f"Falha ao baixar imagem {message_id}: {e}")
        return [{"type": "text", "text": "[imagem não disponível]"}]
