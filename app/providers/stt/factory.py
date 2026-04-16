from functools import lru_cache
from app.providers.stt.base import STTProvider
from app.config import get_settings


@lru_cache(maxsize=1)
def get_stt() -> STTProvider:
    """Retorna instância do STT configurado no .env."""
    settings = get_settings()
    provider = settings.stt_provider
    model = settings.stt_model

    if provider == "groq":
        from app.providers.stt.groq_whisper import GroqWhisperSTT
        return GroqWhisperSTT(api_key=settings.groq_api_key, model=model)

    if provider == "openai":
        from app.providers.stt.openai_whisper import OpenAIWhisperSTT
        return OpenAIWhisperSTT(api_key=settings.openai_api_key, model=model)

    if provider == "local":
        from app.providers.stt.local_whisper import LocalWhisperSTT
        return LocalWhisperSTT(model=model)

    raise ValueError(f"STT provider desconhecido: {provider}")
