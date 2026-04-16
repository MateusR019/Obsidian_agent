"""Indexação de notas do vault no SQLite (metadados + embeddings)."""
import json
import struct
import time
from pathlib import Path

from app.config import get_settings
from app.db.connection import get_connection
from app.indexer.chunker import chunk_markdown
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _get_embed():
    from app.providers.embed.factory import get_embedding
    return get_embedding()


def _vault_root() -> Path:
    return Path(get_settings().vault_path).resolve()


def _pack_embedding(vec: list[float]) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec)


def _upsert_file(conn, path: str, title: str, tipo: str, area: str, tags: str, mtime: float) -> int:
    conn.execute("""
        INSERT INTO vault_files (path, title, tipo, area, tags, mtime)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(path) DO UPDATE SET
            title=excluded.title, tipo=excluded.tipo, area=excluded.area,
            tags=excluded.tags, mtime=excluded.mtime
    """, (path, title, tipo, area, tags, mtime))
    row = conn.execute("SELECT id FROM vault_files WHERE path=?", (path,)).fetchone()
    return row["id"]


def index_note(path: str) -> int:
    """Indexa nota única. Retorna número de chunks criados."""
    vault = _vault_root()
    abs_path = vault / path

    if not abs_path.exists():
        raise FileNotFoundError(path)

    from app.vault.frontmatter import read_frontmatter
    meta, body = read_frontmatter(abs_path)
    mtime = abs_path.stat().st_mtime

    conn = get_connection()
    title = abs_path.stem.replace("_", " ")
    tags_str = json.dumps(meta.tags)

    file_id = _upsert_file(conn, path, title, meta.tipo, meta.area, tags_str, mtime)

    # Remove chunks antigos
    conn.execute("DELETE FROM vec_chunks WHERE file_id=?", (file_id,))

    full_text = f"# {title}\n\n{body}".strip()
    chunks = chunk_markdown(full_text)
    if not chunks:
        conn.commit()
        return 0

    try:
        embedder = _get_embed()
        vectors = embedder.embed(chunks)
        for i, (chunk, vec) in enumerate(zip(chunks, vectors)):
            conn.execute(
                "INSERT INTO vec_chunks (file_id, chunk_index, chunk_text, embedding) VALUES (?,?,?,?)",
                (file_id, i, chunk, _pack_embedding(vec)),
            )
    except Exception as e:
        logger.warning(f"Embedding falhou para {path}: {e} — salvando só texto")
        for i, chunk in enumerate(chunks):
            conn.execute(
                "INSERT INTO vec_chunks (file_id, chunk_index, chunk_text, embedding) VALUES (?,?,?,NULL)",
                (file_id, i, chunk),
            )

    conn.execute(
        "UPDATE vault_files SET indexed_at=datetime('now') WHERE id=?", (file_id,)
    )
    conn.commit()
    return len(chunks)


def index_all(show_progress: bool = True) -> dict[str, int]:
    """Indexa todas as notas do vault. Retorna estatísticas."""
    vault = _vault_root()
    notes = [
        p for p in vault.rglob("*.md")
        if "_SYSTEM" not in p.parts
    ]

    stats = {"total": len(notes), "indexed": 0, "errors": 0}

    for i, p in enumerate(notes, 1):
        rel = str(p.relative_to(vault)).replace("\\", "/")
        try:
            count = index_note(rel)
            stats["indexed"] += 1
            if show_progress:
                logger.info(f"[{i}/{stats['total']}] {rel} — {count} chunks")
        except Exception as e:
            logger.error(f"Erro indexando {rel}: {e}")
            stats["errors"] += 1

    return stats


def reindex_modified() -> dict[str, int]:
    """Re-indexa apenas notas modificadas desde a última indexação."""
    vault = _vault_root()
    conn = get_connection()
    stats = {"checked": 0, "reindexed": 0, "errors": 0}

    for p in vault.rglob("*.md"):
        if "_SYSTEM" in p.parts:
            continue
        rel = str(p.relative_to(vault)).replace("\\", "/")
        mtime = p.stat().st_mtime
        stats["checked"] += 1

        row = conn.execute(
            "SELECT mtime FROM vault_files WHERE path=?", (rel,)
        ).fetchone()

        if row is None or row["mtime"] != mtime:
            try:
                index_note(rel)
                stats["reindexed"] += 1
            except Exception as e:
                logger.error(f"Erro re-indexando {rel}: {e}")
                stats["errors"] += 1

    return stats
