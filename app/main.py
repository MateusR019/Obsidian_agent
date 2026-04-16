import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import get_settings
from app.db.migrations import run_migrations
from app.utils.logger import get_logger
from app.webhook.routes import router as webhook_router
from app.webhook.admin import admin_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info(f"Starting Segundo Cérebro — env={settings.app_env} provider={settings.llm_provider}")
    run_migrations()

    # Inicia watcher de filesystem
    from app.agent.watcher import start_watcher, stop_watcher
    start_watcher()

    # Inicia background tasks
    from app.agent.background import git_autosync_loop, daily_note_check_loop
    asyncio.create_task(git_autosync_loop())
    asyncio.create_task(daily_note_check_loop())

    yield
    stop_watcher()
    logger.info("Shutting down")


app = FastAPI(
    title="Segundo Cérebro",
    description="Agente de IA para organização e consulta de vault Obsidian via WhatsApp",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(webhook_router)
app.include_router(admin_router)


@app.get("/health")
def health():
    settings = get_settings()
    return {
        "status": "ok",
        "service": "segundo-cerebro",
        "llm_provider": settings.llm_provider,
        "llm_model": settings.llm_model or "default",
    }
