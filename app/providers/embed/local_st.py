"""Embeddings locais via sentence-transformers (requer instalação separada)."""
from app.providers.embed.base import EmbeddingProvider


class LocalSTEmbedding(EmbeddingProvider):
    dimension = 384

    def __init__(self, model: str = ""):
        raise NotImplementedError(
            "Embedding local não implementado. Instale 'sentence-transformers' e configure "
            "EMBEDDING_PROVIDER=local. Use EMBEDDING_PROVIDER=gemini para começar."
        )

    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError
