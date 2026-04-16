"""Embeddings via Gemini Embedding API."""
import httpx
from app.providers.embed.base import EmbeddingProvider
from app.utils.logger import get_logger

logger = get_logger(__name__)

GEMINI_EMBED_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
DEFAULT_MODEL = "text-embedding-004"
DEFAULT_DIMENSION = 768


class GeminiEmbedding(EmbeddingProvider):
    def __init__(self, api_key: str, model: str = "", dimension: int = DEFAULT_DIMENSION):
        if not api_key:
            raise ValueError("GEMINI_API_KEY não configurada")
        self._api_key = api_key
        self._model = model or DEFAULT_MODEL
        self.dimension = dimension

    def embed(self, texts: list[str]) -> list[list[float]]:
        url = f"{GEMINI_EMBED_BASE}/{self._model}:batchEmbedContents?key={self._api_key}"
        payload = {
            "requests": [
                {
                    "model": f"models/{self._model}",
                    "content": {"parts": [{"text": t}]},
                    "taskType": "RETRIEVAL_DOCUMENT",
                }
                for t in texts
            ]
        }
        resp = httpx.post(url, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return [item["values"] for item in data["embeddings"]]
