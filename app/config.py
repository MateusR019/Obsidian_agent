from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Geral
    app_env: Literal["development", "production"] = "development"
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000

    # Vault
    vault_path: str = "./vault"
    vault_git_remote: str = ""
    vault_git_branch: str = "main"

    # Banco
    db_path: str = "./data/data.db"

    # Autorização WhatsApp
    allowed_numbers: str = ""
    webhook_secret: str = ""

    # Evolution API
    evolution_url: str = "http://localhost:8080"
    evolution_instance: str = "segundo-cerebro"
    evolution_api_key: str = ""

    # Provider LLM
    llm_provider: Literal["gemini", "groq", "openrouter", "claude", "openai", "nvidia"] = "gemini"
    llm_model: str = ""
    gemini_api_key: str = ""
    groq_api_key: str = ""
    openrouter_api_key: str = ""
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    nvidia_api_key: str = ""

    # Provider STT
    stt_provider: Literal["groq", "openai", "local"] = "groq"
    stt_model: str = ""

    # Provider Embedding
    embedding_provider: Literal["gemini", "openai", "local"] = "gemini"
    embedding_model: str = ""
    embedding_dimension: int = 768

    # Agente
    agent_max_tool_iterations: int = 5
    agent_history_window: int = 20
    agent_temperature: float = 0.3

    @property
    def allowed_numbers_list(self) -> list[str]:
        return [n.strip() for n in self.allowed_numbers.split(",") if n.strip()]


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
