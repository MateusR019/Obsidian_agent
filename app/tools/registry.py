"""Registro central de tools disponíveis para o agente."""
from dataclasses import dataclass, field
from typing import Callable, Any
from app.providers.llm.base import ToolDef

_registry: dict[str, "_ToolEntry"] = {}


@dataclass
class _ToolEntry:
    name: str
    description: str
    schema: dict
    fn: Callable


def tool(name: str, description: str, schema: dict):
    """Decorator que registra uma função como tool do agente."""
    def decorator(fn: Callable) -> Callable:
        _registry[name] = _ToolEntry(name=name, description=description, schema=schema, fn=fn)
        return fn
    return decorator


def get_tool_defs() -> list[ToolDef]:
    return [
        ToolDef(name=e.name, description=e.description, parameters=e.schema)
        for e in _registry.values()
    ]


def execute_tool(name: str, arguments: dict) -> Any:
    """Executa tool pelo nome com os argumentos fornecidos."""
    entry = _registry.get(name)
    if not entry:
        raise ValueError(f"Tool desconhecida: {name}")
    return entry.fn(**arguments)
