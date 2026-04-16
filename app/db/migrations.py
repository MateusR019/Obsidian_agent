from app.db.connection import get_connection
from app.db.models import (
    SCHEMA_MESSAGES,
    SCHEMA_SESSIONS,
    SCHEMA_VAULT_FILES,
    SCHEMA_VEC_CHUNKS,
)
from app.utils.logger import get_logger

logger = get_logger(__name__)


def run_migrations() -> None:
    """Cria tabelas se não existirem."""
    conn = get_connection()
    for schema in (SCHEMA_MESSAGES, SCHEMA_SESSIONS, SCHEMA_VAULT_FILES, SCHEMA_VEC_CHUNKS):
        for statement in schema.strip().split(";"):
            stmt = statement.strip()
            if stmt:
                conn.execute(stmt)
    conn.commit()
    logger.info("Database migrations complete")
