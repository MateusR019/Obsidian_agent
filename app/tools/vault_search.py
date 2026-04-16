from app.tools.registry import tool
from app.indexer.search import search

@tool(
    name="vault_search",
    description="Busca notas no vault por relevância semântica e keyword.",
    schema={
        "type": "object",
        "properties": {
            "query":       {"type": "string", "description": "Texto de busca"},
            "folder":      {"type": "string", "description": "Limita busca a uma pasta específica"},
            "top_k":       {"type": "integer", "description": "Número de resultados (padrão 5)", "default": 5},
            "filter_tipo": {"type": "string", "description": "Filtra por tipo de nota"},
            "filter_area": {"type": "string", "description": "Filtra por área/marca"},
        },
        "required": ["query"],
    },
)
def vault_search(
    query: str,
    folder: str | None = None,
    top_k: int = 5,
    filter_tipo: str | None = None,
    filter_area: str | None = None,
) -> dict:
    results = search(query=query, top_k=top_k, folder=folder, filter_tipo=filter_tipo, filter_area=filter_area)
    return {
        "count": len(results),
        "results": [
            {
                "path": r.path,
                "title": r.title,
                "score": r.score,
                "tipo": r.tipo,
                "area": r.area,
                "excerpt": r.chunk_text[:300],
            }
            for r in results
        ],
    }
