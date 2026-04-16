import logging
import sys
from app.config import get_settings

try:
    from rich.logging import RichHandler
    _rich_available = True
except ImportError:
    _rich_available = False


def get_logger(name: str) -> logging.Logger:
    """Retorna logger configurado para o módulo informado."""
    settings = get_settings()
    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)

    if _rich_available and settings.app_env == "development":
        handler = RichHandler(rich_tracebacks=True, markup=True)
        fmt = "%(message)s"
    else:
        handler = logging.StreamHandler(sys.stdout)
        fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    logger.propagate = False
    return logger
