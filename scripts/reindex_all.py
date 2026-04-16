"""Reindexa todo o vault. Útil após bulk import de notas."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.db.migrations import run_migrations
from app.indexer.indexer import index_all
from app.utils.logger import get_logger

logger = get_logger("reindex")


def main() -> None:
    run_migrations()
    logger.info("Iniciando reindexação completa do vault...")
    stats = index_all(show_progress=True)
    logger.info(f"Concluído: {stats['indexed']}/{stats['total']} notas | erros: {stats['errors']}")


if __name__ == "__main__":
    main()
