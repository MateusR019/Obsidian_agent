from datetime import date
from app.tools.registry import tool
from app.vault.manager import get_vault_manager
from app.vault.templates import apply_template

@tool(
    name="daily_note",
    description="Cria ou retorna a daily note do dia (ou de uma data específica).",
    schema={
        "type": "object",
        "properties": {
            "date": {"type": "string", "description": "Data no formato YYYY-MM-DD (padrão: hoje)"},
        },
        "required": [],
    },
)
def daily_note(date: str | None = None) -> dict:
    target = date or str(__import__("datetime").date.today())
    try:
        d = __import__("datetime").date.fromisoformat(target)
    except ValueError:
        return {"ok": False, "error": f"Data inválida: {target}"}

    folder = f"10_Daily/{d.year}/{d.month:02d}"
    filename = target  # ex: 2026-04-16

    vm = get_vault_manager()
    path = f"{folder}/{filename}.md"

    try:
        note = vm.read_note(path)
        return {"ok": True, "path": note.path, "exists": True, "content": note.content[:500]}
    except FileNotFoundError:
        pass

    try:
        content = apply_template("daily", {"data": target, "titulo": f"Daily — {target}"})
    except FileNotFoundError:
        content = f"# Daily — {target}\n\n## Prioridades do Dia\n- [ ] \n\n## Notas\n"

    note = vm.create_note(
        folder=folder,
        filename=filename,
        content=content,
        frontmatter_data={"tipo": "daily", "area": "pessoal", "tags": ["daily"]},
    )
    return {"ok": True, "path": note.path, "exists": False, "message": f"Daily note criada: {note.path}"}
