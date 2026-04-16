"""API alto-nível para criar, ler, atualizar e listar notas do vault."""
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any
import re

from app.config import get_settings
from app.vault.frontmatter import NoteFrontmatter, read_frontmatter, write_frontmatter
from app.vault import git_sync
from app.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Note:
    path: str          # relativo ao vault
    title: str
    content: str
    frontmatter: NoteFrontmatter
    abs_path: Path = field(repr=False, default=None)  # type: ignore


def _vault_root() -> Path:
    return Path(get_settings().vault_path).resolve()


def _sanitize_filename(name: str) -> str:
    """Remove caracteres inválidos para nome de arquivo."""
    name = name.strip()
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = re.sub(r"\s+", "_", name)
    return name or "nota"


def _safe_path(vault: Path, rel: str) -> Path:
    """Valida que o path não escapa do vault."""
    target = (vault / rel).resolve()
    if not str(target).startswith(str(vault)):
        raise ValueError(f"Path inválido (fora do vault): {rel}")
    return target


class VaultManager:
    def __init__(self) -> None:
        self._vault = _vault_root()

    def create_note(
        self,
        folder: str,
        filename: str,
        content: str,
        title: str = "",
        frontmatter_data: dict[str, Any] | None = None,
    ) -> Note:
        """Cria nota nova. Se já existir, levanta FileExistsError."""
        clean_name = _sanitize_filename(filename)
        if not clean_name.endswith(".md"):
            clean_name += ".md"

        rel = f"{folder.strip('/')}/{clean_name}"
        abs_path = _safe_path(self._vault, rel)
        abs_path.parent.mkdir(parents=True, exist_ok=True)

        if abs_path.exists():
            raise FileExistsError(f"Nota já existe: {rel}")

        meta = NoteFrontmatter.from_dict(frontmatter_data or {})
        if not meta.criado:
            meta.criado = date.today().isoformat()

        write_frontmatter(abs_path, meta, content)
        logger.info(f"Note created: {rel}")
        git_sync.commit_and_push()
        return self._load(abs_path, rel)

    def read_note(self, path: str) -> Note:
        """Lê nota pelo path relativo ao vault."""
        abs_path = _safe_path(self._vault, path)
        if not abs_path.exists():
            raise FileNotFoundError(f"Nota não encontrada: {path}")
        return self._load(abs_path, path)

    def update_note(
        self,
        path: str,
        content: str | None = None,
        append: str | None = None,
        prepend: str | None = None,
        frontmatter_patch: dict[str, Any] | None = None,
    ) -> Note:
        """
        Atualiza nota existente.
        - content: substitui corpo inteiro
        - append: adiciona ao final
        - prepend: adiciona ao início
        - frontmatter_patch: atualiza campos específicos do frontmatter
        """
        abs_path = _safe_path(self._vault, path)
        if not abs_path.exists():
            raise FileNotFoundError(f"Nota não encontrada: {path}")

        meta, body = read_frontmatter(abs_path)

        if content is not None:
            body = content
        if append:
            body = body.rstrip("\n") + "\n\n" + append
        if prepend:
            body = prepend + "\n\n" + body.lstrip("\n")

        if frontmatter_patch:
            for k, v in frontmatter_patch.items():
                if hasattr(meta, k):
                    setattr(meta, k, v)
                else:
                    meta.extra[k] = v

        write_frontmatter(abs_path, meta, body)
        logger.info(f"Note updated: {path}")
        git_sync.commit_and_push()
        return self._load(abs_path, path)

    def list_notes(
        self,
        folder: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 50,
    ) -> list[Note]:
        """Lista notas de uma pasta (ou vault inteiro) com filtros opcionais."""
        base = _safe_path(self._vault, folder) if folder else self._vault
        if not base.exists():
            return []

        notes: list[Note] = []
        for p in sorted(base.rglob("*.md")):
            if "_SYSTEM" in p.parts:
                continue
            rel = str(p.relative_to(self._vault)).replace("\\", "/")
            try:
                note = self._load(p, rel)
            except Exception:
                continue

            if filters:
                match = True
                for k, v in filters.items():
                    fm_val = getattr(note.frontmatter, k, None) or note.frontmatter.extra.get(k)
                    if fm_val != v:
                        match = False
                        break
                if not match:
                    continue

            notes.append(note)
            if len(notes) >= limit:
                break

        return notes

    def _load(self, abs_path: Path, rel: str) -> Note:
        meta, body = read_frontmatter(abs_path)
        title = meta.extra.get("title") or abs_path.stem.replace("_", " ")
        return Note(
            path=rel,
            title=title,
            content=body,
            frontmatter=meta,
            abs_path=abs_path,
        )


_manager: VaultManager | None = None


def get_vault_manager() -> VaultManager:
    global _manager
    if _manager is None:
        _manager = VaultManager()
    return _manager
