"""Download e extração de texto de PDFs."""
import io
import httpx
import base64
from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


def extract_pdf_text(message_id: str) -> str:
    """Baixa PDF da Evolution API e extrai texto com pypdf."""
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
        pdf_bytes = base64.b64decode(b64)
    except Exception as e:
        logger.error(f"Falha ao baixar PDF {message_id}: {e}")
        return "[PDF não disponível]"

    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        pages = []
        for page in reader.pages:
            text = page.extract_text() or ""
            if text.strip():
                pages.append(text.strip())
        result = "\n\n".join(pages)
        logger.info(f"PDF extraído: {len(result)} chars, {len(pages)} páginas")
        return result or "[PDF sem texto extraível]"
    except Exception as e:
        logger.error(f"pypdf falhou para {message_id}: {e}")
        return "[erro ao extrair texto do PDF]"
