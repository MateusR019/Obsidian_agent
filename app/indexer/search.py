"""Busca híbrida: vetorial (sqlite-vec) + BM25 keyword com Reciprocal Rank Fusion."""
import json
import struct
from dataclasses import dataclass

from rank_bm25 import BM25Okapi

from app.db.connection import get_connection
from app.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class SearchResult:
    path: str
    title: str
    chunk_text: str
    score: float
    tipo: str
    area: str


def _pack_embedding(vec: list[float]) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec)


def _get_embed():
    from app.providers.embed.factory import get_embedding
    return get_embedding()


def _bm25_search(query: str, candidates: list[dict], top_k: int) -> list[tuple[int, float]]:
    """Retorna lista de (chunk_id, score) por BM25."""
    if not candidates:
        return []
    tokenized = [c["chunk_text"].lower().split() for c in candidates]
    bm25 = BM25Okapi(tokenized)
    scores = bm25.get_scores(query.lower().split())
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    return [(candidates[i]["id"], float(s)) for i, s in ranked[:top_k]]


def _vector_search(query: str, top_k: int, filter_sql: str, filter_params: list) -> list[tuple[int, float]]:
    """Busca vetorial usando cosine similarity manual (sqlite-vec pode não estar disponível)."""
    try:
        embedder = _get_embed()
        q_vec = embedder.embed([query])[0]
    except Exception as e:
        logger.warning(f"Embedding da query falhou: {e}")
        return []

    conn = get_connection()
    rows = conn.execute(
        f"SELECT vc.id, vc.embedding FROM vec_chunks vc "
        f"JOIN vault_files vf ON vc.file_id = vf.id "
        f"{filter_sql} AND vc.embedding IS NOT NULL",
        filter_params,
    ).fetchall()

    if not rows:
        return []

    import math

    def cosine(a: list[float], b_bytes: bytes) -> float:
        n = len(a)
        b = list(struct.unpack(f"{n}f", b_bytes[:n * 4]))
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(x * x for x in b))
        if na == 0 or nb == 0:
            return 0.0
        return dot / (na * nb)

    scored = [(row["id"], cosine(q_vec, row["embedding"])) for row in rows]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


def _reciprocal_rank_fusion(
    ranked_lists: list[list[tuple[int, float]]],
    k: int = 60,
) -> list[tuple[int, float]]:
    """Combina múltiplos rankings via RRF."""
    scores: dict[int, float] = {}
    for ranked in ranked_lists:
        for rank, (doc_id, _) in enumerate(ranked, 1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def search(
    query: str,
    top_k: int = 5,
    folder: str | None = None,
    filter_tipo: str | None = None,
    filter_area: str | None = None,
) -> list[SearchResult]:
    """
    Busca híbrida (vetorial + BM25) com RRF.
    Retorna top_k resultados ordenados por relevância.
    """
    conn = get_connection()

    # Monta filtro SQL
    conditions = ["1=1"]
    params: list = []
    if folder:
        conditions.append("vf.path LIKE ?")
        params.append(f"{folder.strip('/')}/%")
    if filter_tipo:
        conditions.append("vf.tipo = ?")
        params.append(filter_tipo)
    if filter_area:
        conditions.append("vf.area = ?")
        params.append(filter_area)

    where = "WHERE " + " AND ".join(conditions)

    # Busca candidatos
    candidates = conn.execute(
        f"SELECT vc.id, vc.chunk_text, vf.path, vf.title, vf.tipo, vf.area "
        f"FROM vec_chunks vc JOIN vault_files vf ON vc.file_id = vf.id {where}",
        params,
    ).fetchall()
    candidates = [dict(c) for c in candidates]

    if not candidates:
        return []

    # BM25
    bm25_results = _bm25_search(query, candidates, top_k * 2)

    # Vetorial
    vec_results = _vector_search(query, top_k * 2, where, params)

    # RRF
    fused = _reciprocal_rank_fusion([bm25_results, vec_results])[:top_k]

    chunk_map = {c["id"]: c for c in candidates}
    results: list[SearchResult] = []
    for chunk_id, score in fused:
        c = chunk_map.get(chunk_id)
        if c:
            results.append(SearchResult(
                path=c["path"],
                title=c["title"] or "",
                chunk_text=c["chunk_text"],
                score=round(score, 4),
                tipo=c["tipo"] or "",
                area=c["area"] or "",
            ))

    return results
