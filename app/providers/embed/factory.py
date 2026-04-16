from functools import lru_cache
from app.providers.embed.base import EmbeddingProvider
from app.config import get_settings


@lru_cache(maxsize=1)
def get_embedding() -> EmbeddingProvider:
    """Retorna instância do provider de embeddings configurado no .env."""
    settings = get_settings()
    provider = settings.embedding_provider
    model = settings.embedding_model
    dimension = settings.embedding_dimension

    if provider == "gemini":
        from app.providers.embed.gemini import GeminiEmbedding
        return GeminiEmbedding(api_key=settings.gemini_api_key, model=model, dimension=dimension)

    if provider == "openai":
        from app.providers.embed.openai import OpenAIEmbedding
        return OpenAIEmbedding(api_key=settings.openai_api_key, model=model, dimension=dimension)

    if provider == "local":
        from app.providers.embed.local_st import LocalSTEmbedding
        return LocalSTEmbedding(model=model)

    raise ValueError(f"Embedding provider desconhecido: {provider}")
