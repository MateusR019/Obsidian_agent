from app.tools.registry import tool
from app.vault.manager import get_vault_manager

@tool(
    name="vault_read",
    description="Lê o conteúdo de uma nota do vault pelo path.",
    schema={
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Path relativo ao vault (ex: '20_Operacao/EFish/Produtos/Motor.md')"},
        },
        "required": ["path"],
    },
)
def vault_read(path: str) -> dict:
    vm = get_vault_manager()
    note = vm.read_note(path)
    return {
        "path": note.path,
        "title": note.title,
        "content": note.content,
        "frontmatter": note.frontmatter.to_dict(),
    }
