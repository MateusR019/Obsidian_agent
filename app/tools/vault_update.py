from typing import Literal
from app.tools.registry import tool
from app.vault.manager import get_vault_manager

@tool(
    name="vault_update",
    description="Edita uma nota existente no vault.",
    schema={
        "type": "object",
        "properties": {
            "path":    {"type": "string", "description": "Path relativo da nota"},
            "mode":    {"type": "string", "enum": ["replace", "append", "prepend"], "description": "Modo de edição"},
            "content": {"type": "string", "description": "Conteúdo a inserir/substituir"},
            "frontmatter_patch": {
                "type": "object",
                "description": "Campos do frontmatter para atualizar (ex: {\"status\": \"arquivado\"})",
            },
        },
        "required": ["path", "mode", "content"],
    },
)
def vault_update(
    path: str,
    mode: Literal["replace", "append", "prepend"],
    content: str,
    frontmatter_patch: dict | None = None,
) -> dict:
    vm = get_vault_manager()
    note = vm.update_note(
        path=path,
        content=content if mode == "replace" else None,
        append=content if mode == "append" else None,
        prepend=content if mode == "prepend" else None,
        frontmatter_patch=frontmatter_patch,
    )
    return {"ok": True, "path": note.path, "message": f"Nota atualizada: {note.path}"}
