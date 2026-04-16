"""Leitura e escrita de YAML frontmatter em notas Obsidian."""
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any
import frontmatter as fm


@dataclass
class NoteFrontmatter:
    tipo: str = ""
    area: str = ""
    criado: str = ""
    atualizado: str = ""
    fonte: str = ""
    tags: list[str] = field(default_factory=list)
    status: str = ""
    links_relacionados: list[str] = field(default_factory=list)
    extra: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        d: dict[str, Any] = {}
        if self.tipo:
            d["tipo"] = self.tipo
        if self.area:
            d["area"] = self.area
        if self.criado:
            d["criado"] = self.criado
        if self.atualizado:
            d["atualizado"] = self.atualizado
        if self.fonte:
            d["fonte"] = self.fonte
        if self.tags:
            d["tags"] = self.tags
        if self.status:
            d["status"] = self.status
        if self.links_relacionados:
            d["links_relacionados"] = self.links_relacionados
        d.update(self.extra)
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "NoteFrontmatter":
        known = {"tipo", "area", "criado", "atualizado", "fonte", "tags", "status", "links_relacionados"}
        extra = {k: v for k, v in data.items() if k not in known}
        return cls(
            tipo=str(data.get("tipo", "")),
            area=str(data.get("area", "")),
            criado=str(data.get("criado", "")),
            atualizado=str(data.get("atualizado", "")),
            fonte=str(data.get("fonte", "")),
            tags=list(data.get("tags") or []),
            status=str(data.get("status", "")),
            links_relacionados=list(data.get("links_relacionados") or []),
            extra=extra,
        )


def read_frontmatter(path: Path) -> tuple[NoteFrontmatter, str]:
    """Lê arquivo .md e retorna (frontmatter, body)."""
    post = fm.load(str(path))
    return NoteFrontmatter.from_dict(dict(post.metadata)), post.content


def write_frontmatter(path: Path, meta: NoteFrontmatter, body: str) -> None:
    """Escreve nota .md com frontmatter atualizado."""
    today = date.today().isoformat()
    meta_dict = meta.to_dict()
    if not meta_dict.get("criado"):
        meta_dict["criado"] = today
    meta_dict["atualizado"] = today

    post = fm.Post(body, **meta_dict)
    path.write_text(fm.dumps(post), encoding="utf-8")
