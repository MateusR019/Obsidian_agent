"""Reindexa todo o vault. Útil após bulk import de notas."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.utils.logger import get_logger

logger = get_logger("reindex")


def main() -> None:
    logger.info("Reindex all — será implementado na Fase 3")


if __name__ == "__main__":
    main()
