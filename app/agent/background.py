"""Tasks em background: git auto-sync a cada 5min."""
import asyncio
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def git_autosync_loop() -> None:
    """Faz commit+push do vault a cada 5 minutos se houver mudanças."""
    from app.vault.git_sync import commit_and_push
    while True:
        await asyncio.sleep(300)  # 5 min
        try:
            commit_and_push(immediate=True)
        except Exception as e:
            logger.error(f"Git autosync falhou: {e}")


async def daily_note_check_loop() -> None:
    """Garante que a daily note de hoje existe (verifica na primeira interação do dia)."""
    # A daily note é criada via tool pelo agente; esta task é só um log de confirmação
    import asyncio
    from datetime import date
    last_checked: str = ""
    while True:
        await asyncio.sleep(3600)  # a cada hora
        today = str(date.today())
        if today != last_checked:
            last_checked = today
            logger.info(f"Novo dia: {today} — daily note será criada na primeira interação")
