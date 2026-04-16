"""
Cria estrutura inicial do vault Obsidian e inicializa o banco.

Edite VAULT_FOLDERS abaixo para adaptar à sua realidade antes de rodar.
"""
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import get_settings
from app.db.migrations import run_migrations
from app.utils.logger import get_logger

logger = get_logger("setup")

# ─── Personalize aqui ────────────────────────────────────────────────────────
# Estrutura de pastas do seu vault. Adicione ou remova conforme sua necessidade.
VAULT_FOLDERS = [
    "00_Inbox",
    f"10_Daily/{date.today().year}/{date.today().month:02d}",
    "20_Work/Projects",
    "20_Work/Clients",
    "20_Work/Documents",
    "30_Personal/Finance",
    "30_Personal/Health",
    "30_Personal/Hobbies",
    "30_Personal/Journal",
    "40_Knowledge",
    "50_People",
    "60_Archive",
    "_SYSTEM/templates",
]
# ─────────────────────────────────────────────────────────────────────────────

REGRAS_MD = """\
# Agent Rules

## Identity
You are the user's Second Brain — a personal assistant that organizes
knowledge in an Obsidian vault and responds via WhatsApp.

## Tone & Communication
- Be concise and direct
- Confirm before performing irreversible actions
- Ask when uncertain about where to file new content

## When to Act vs When to Ask
- **Act directly**: create note, log cost, search info, daily note
- **Ask first**: delete note, overwrite critical data
- **Never assume**: if unsure about the right folder, ask

## Default Folders
- New inbox items → `00_Inbox/`
- Daily notes → `10_Daily/<year>/<month>/`
- Work files → `20_Work/`
- Personal → `30_Personal/`

## Note Structure
- Always use YAML frontmatter: tipo, area, criado, atualizado, tags
- Use PascalCase filenames without spaces
- Use templates from `_SYSTEM/templates/` when available
"""

GLOSSARIO_MD = """\
# Glossary

Add your domain-specific terms here so the agent understands your context.

## Example
- **Term**: Definition
- **Acronym**: What it stands for
"""

CONTEXTO_NEGOCIO_MD = """\
# Business / Personal Context

Describe yourself and your context here so the agent can serve you better.

## About Me
- Role / occupation:
- Main areas of focus:
- Tools I use:

## Goals
- What I want to use this Second Brain for:

## Notes
- Any other context the agent should know:
"""

TEMPLATE_DAILY = """\
---
tipo: daily
area: personal
criado: {{data}}
atualizado: {{data}}
tags: [daily]
---

# Daily — {{data}}

## Priorities
- [ ]
- [ ]

## Meetings / Events
-

## Notes
"""

TEMPLATE_NOTE = """\
---
tipo: note
area:
criado: {{data}}
atualizado: {{data}}
tags: []
status: active
links_relacionados: []
---

# {{titulo}}

## Summary

## Details

## Next Steps
- [ ]
"""

TEMPLATE_PROJECT = """\
---
tipo: projeto
area:
criado: {{data}}
atualizado: {{data}}
tags: []
status: em_andamento
links_relacionados: []
---

# {{titulo}}

## Goal
## Context
## Next Steps
- [ ]
## Log
"""

TEMPLATE_PERSON = """\
---
tipo: pessoa
area:
criado: {{data}}
atualizado: {{data}}
tags: []
status: ativo
links_relacionados: []
---

# {{titulo}}

## Details
- **Company / Role**:
- **Email**:
- **Phone / WhatsApp**:

## Context
"""

TEMPLATE_INBOX = """\
---
tipo: inbox
area:
criado: {{data}}
atualizado: {{data}}
tags: []
status: para_classificar
---

# {{titulo}}

{{conteudo}}
"""

TEMPLATES = {
    "_daily.md": TEMPLATE_DAILY,
    "_note.md": TEMPLATE_NOTE,
    "_project.md": TEMPLATE_PROJECT,
    "_person.md": TEMPLATE_PERSON,
    "_inbox.md": TEMPLATE_INBOX,
}


def create_vault_structure(vault: Path) -> None:
    logger.info(f"Creating vault at {vault}")
    for folder in VAULT_FOLDERS:
        folder_path = vault / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        gitkeep = folder_path / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()

    system = vault / "_SYSTEM"
    (system / "regras.md").write_text(REGRAS_MD, encoding="utf-8")
    (system / "glossario.md").write_text(GLOSSARIO_MD, encoding="utf-8")
    (system / "contexto_negocio.md").write_text(CONTEXTO_NEGOCIO_MD, encoding="utf-8")

    for fname, content in TEMPLATES.items():
        (system / "templates" / fname).write_text(content, encoding="utf-8")

    logger.info("Vault structure created")


def main() -> None:
    settings = get_settings()
    vault = Path(settings.vault_path).resolve()

    create_vault_structure(vault)
    run_migrations()
    logger.info("Setup complete! Run: uvicorn app.main:app --reload")


if __name__ == "__main__":
    main()
