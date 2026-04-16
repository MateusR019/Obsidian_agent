"""STT local via faster-whisper (requer instalação separada)."""
from app.providers.stt.base import STTProvider


class LocalWhisperSTT(STTProvider):
    def __init__(self, model: str = ""):
        raise NotImplementedError(
            "STT local não implementado. Instale 'faster-whisper' e configure STT_PROVIDER=local. "
            "Use STT_PROVIDER=groq ou openai para começar."
        )

    def transcribe(self, audio_bytes: bytes, mime_type: str = "audio/ogg") -> str:
        raise NotImplementedError
