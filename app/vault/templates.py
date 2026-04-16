"""Carrega e aplica templates de _SYSTEM/templates/."""
from datetime import date
from pathlib import Path
from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _templates_dir() -> Path:
    settings = get_settings()
    return Path(settings.vault_path) / "_SYSTEM" / "templates"


def list_templates() -> list[str]:
    d = _templates_dir()
    if not d.exists():
        return []
    return [p.stem.lstrip("_") for p in d.glob("_*.md")]


def apply_template(template_name: str, variables: dict[str, str] | None = None) -> str:
    """Carrega template e substitui {{variavel}} pelos valores fornecidos."""
    d = _templates_dir()
    path = d / f"_{template_name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Template não encontrado: {template_name}")

    content = path.read_text(encoding="utf-8")
    vars_ = {"data": date.today().isoformat(), "titulo": ""}
    if variables:
        vars_.update(variables)

    for key, value in vars_.items():
        content = content.replace("{{" + key + "}}", value)

    return content
