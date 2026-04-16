from functools import lru_cache
from app.providers.llm.base import LLMProvider
from app.config import get_settings


@lru_cache(maxsize=1)
def get_llm() -> LLMProvider:
    """Retorna instância do LLM configurado no .env."""
    settings = get_settings()
    provider = settings.llm_provider
    model = settings.llm_model

    if provider == "gemini":
        from app.providers.llm.gemini import GeminiLLM
        return GeminiLLM(api_key=settings.gemini_api_key, model=model)

    if provider == "groq":
        from app.providers.llm.groq import GroqLLM
        return GroqLLM(api_key=settings.groq_api_key, model=model)

    if provider == "openai":
        from app.providers.llm.openai import OpenAILLM
        return OpenAILLM(api_key=settings.openai_api_key, model=model)

    if provider == "openrouter":
        from app.providers.llm.openrouter import OpenRouterLLM
        return OpenRouterLLM(api_key=settings.openrouter_api_key, model=model)

    if provider == "claude":
        from app.providers.llm.claude import ClaudeLLM
        return ClaudeLLM(api_key=settings.anthropic_api_key, model=model)

    raise ValueError(f"LLM provider desconhecido: {provider}")
