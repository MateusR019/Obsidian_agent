from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    dimension: int

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Gera embeddings para uma lista de textos."""
        ...
