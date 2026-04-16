"""Provider NVIDIA NIM — API compatível com OpenAI."""
from app.providers.llm.openai import OpenAILLM

NVIDIA_BASE = "https://integrate.api.nvidia.com/v1"
DEFAULT_MODEL = "meta/llama-3.3-70b-instruct"


class NvidiaLLM(OpenAILLM):
    def __init__(self, api_key: str, model: str = ""):
        if not api_key:
            raise ValueError("NVIDIA_API_KEY não configurada")
        super().__init__(api_key=api_key, model=model or DEFAULT_MODEL, base_url=NVIDIA_BASE)

    def supports_vision(self) -> bool:
        # Modelos visuais NVIDIA disponíveis, mas depende do modelo escolhido
        return False
