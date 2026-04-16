"""STT via OpenAI Whisper API."""
import httpx
from app.providers.stt.base import STTProvider
from app.utils.logger import get_logger

logger = get_logger(__name__)

OPENAI_STT_URL = "https://api.openai.com/v1/audio/transcriptions"
DEFAULT_MODEL = "whisper-1"


class OpenAIWhisperSTT(STTProvider):
    def __init__(self, api_key: str, model: str = ""):
        if not api_key:
            raise ValueError("OPENAI_API_KEY não configurada")
        self._api_key = api_key
        self._model = model or DEFAULT_MODEL

    def transcribe(self, audio_bytes: bytes, mime_type: str = "audio/ogg") -> str:
        ext = mime_type.split("/")[-1].split(";")[0] or "ogg"
        files = {"file": (f"audio.{ext}", audio_bytes, mime_type)}
        data = {"model": self._model, "language": "pt", "response_format": "text"}

        resp = httpx.post(
            OPENAI_STT_URL,
            headers={"Authorization": f"Bearer {self._api_key}"},
            files=files,
            data=data,
            timeout=60,
        )
        resp.raise_for_status()
        return resp.text.strip()
