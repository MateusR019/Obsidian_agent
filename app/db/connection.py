import sqlite3
from pathlib import Path
from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
_conn: sqlite3.Connection | None = None


def get_connection() -> sqlite3.Connection:
    """Retorna conexão singleton ao SQLite com sqlite-vec carregado."""
    global _conn
    if _conn is not None:
        return _conn

    settings = get_settings()
    db_path = Path(settings.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row

    try:
        import sqlite_vec
        sqlite_vec.load(conn)
        logger.info("sqlite-vec loaded successfully")
    except Exception as e:
        logger.warning(f"sqlite-vec not available: {e} — vector search disabled")

    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    _conn = conn
    return _conn


def close_connection() -> None:
    global _conn
    if _conn:
        _conn.close()
        _conn = None
