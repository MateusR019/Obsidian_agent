from app.tools.registry import tool
from app.vault.manager import get_vault_manager

@tool(
    name="vault_list",
    description="Lista notas de uma pasta do vault.",
    schema={
        "type": "object",
        "properties": {
            "folder": {"type": "string", "description": "Pasta para listar (ex: '20_Operacao/EFish/Produtos')"},
            "limit":  {"type": "integer", "description": "Máximo de resultados (padrão 20)", "default": 20},
        },
        "required": ["folder"],
    },
)
def vault_list(folder: str, limit: int = 20) -> dict:
    vm = get_vault_manager()
    notes = vm.list_notes(folder=folder, limit=limit)
    return {
        "folder": folder,
        "count": len(notes),
        "notes": [
            {"path": n.path, "title": n.title, "tipo": n.frontmatter.tipo, "area": n.frontmatter.area}
            for n in notes
        ],
    }
