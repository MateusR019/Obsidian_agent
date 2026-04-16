"""Provider OpenRouter — reutiliza OpenAILLM com base_url diferente."""
from app.providers.llm.openai import OpenAILLM

OPENROUTER_BASE = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "google/gemini-2.0-flash-001"


class OpenRouterLLM(OpenAILLM):
    def __init__(self, api_key: str, model: str = ""):
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY não configurada")
        super().__init__(api_key=api_key, model=model or DEFAULT_MODEL, base_url=OPENROUTER_BASE)

    def supports_vision(self) -> bool:
        return True
