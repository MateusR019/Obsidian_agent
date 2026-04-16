from app.tools.registry import tool
from app.vault.manager import get_vault_manager

@tool(
    name="vault_create",
    description="Cria uma nova nota no vault Obsidian.",
    schema={
        "type": "object",
        "properties": {
            "folder":   {"type": "string", "description": "Pasta destino (ex: '20_Operacao/EFish/Produtos')"},
            "filename": {"type": "string", "description": "Nome do arquivo sem .md (ex: 'MotorMercury15HP')"},
            "title":    {"type": "string", "description": "Título da nota"},
            "content":  {"type": "string", "description": "Corpo da nota em markdown"},
            "tipo":     {"type": "string", "description": "Tipo da nota (produto, fornecedor, projeto, etc)"},
            "area":     {"type": "string", "description": "Área/marca relacionada (EFish, SeaFishing, etc)"},
            "tags":     {"type": "array", "items": {"type": "string"}, "description": "Tags da nota"},
            "links":    {"type": "array", "items": {"type": "string"}, "description": "Links relacionados"},
        },
        "required": ["folder", "filename", "content"],
    },
)
def vault_create(
    folder: str,
    filename: str,
    content: str,
    title: str = "",
    tipo: str = "",
    area: str = "",
    tags: list[str] | None = None,
    links: list[str] | None = None,
) -> dict:
    vm = get_vault_manager()
    note = vm.create_note(
        folder=folder,
        filename=filename,
        content=content,
        title=title,
        frontmatter_data={
            "tipo": tipo,
            "area": area,
            "tags": tags or [],
            "links_relacionados": links or [],
        },
    )
    return {"ok": True, "path": note.path, "message": f"Nota criada: {note.path}"}
