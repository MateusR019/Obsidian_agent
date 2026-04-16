"""Embeddings via OpenAI."""
import httpx
from app.providers.embed.base import EmbeddingProvider
from app.utils.logger import get_logger

logger = get_logger(__name__)

OPENAI_EMBED_URL = "https://api.openai.com/v1/embeddings"
DEFAULT_MODEL = "text-embedding-3-small"
DEFAULT_DIMENSION = 1536


class OpenAIEmbedding(EmbeddingProvider):
    def __init__(self, api_key: str, model: str = "", dimension: int = DEFAULT_DIMENSION):
        if not api_key:
            raise ValueError("OPENAI_API_KEY não configurada")
        self._api_key = api_key
        self._model = model or DEFAULT_MODEL
        self.dimension = dimension

    def embed(self, texts: list[str]) -> list[list[float]]:
        resp = httpx.post(
            OPENAI_EMBED_URL,
            json={"model": self._model, "input": texts},
            headers={"Authorization": f"Bearer {self._api_key}"},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]
