"""Testa providers configurados no .env."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.utils.logger import get_logger

logger = get_logger("test_providers")


def main() -> None:
    logger.info("Provider tests — será implementado na Fase 2")


if __name__ == "__main__":
    main()
