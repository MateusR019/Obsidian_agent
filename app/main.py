from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import get_settings
from app.db.migrations import run_migrations
from app.utils.logger import get_logger
from app.webhook.routes import router as webhook_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info(f"Starting Segundo Cérebro — env={settings.app_env} provider={settings.llm_provider}")
    run_migrations()
    yield
    logger.info("Shutting down")


app = FastAPI(
    title="Segundo Cérebro",
    description="Agente de IA para organização e consulta de vault Obsidian via WhatsApp",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(webhook_router)


@app.get("/health")
def health():
    settings = get_settings()
    return {
        "status": "ok",
        "service": "segundo-cerebro",
        "llm_provider": settings.llm_provider,
        "llm_model": settings.llm_model or "default",
    }
