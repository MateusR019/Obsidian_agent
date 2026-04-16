from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Message:
    role: str  # "user" | "assistant" | "system" | "tool"
    content: str | list[dict]
    tool_call_id: str | None = None
    tool_calls: list[dict] | None = None


@dataclass
class ToolDef:
    name: str
    description: str
    parameters: dict  # JSON schema


@dataclass
class LLMResponse:
    content: str | None
    tool_calls: list[dict] = field(default_factory=list)  # [{"id":..,"name":..,"arguments":{..}}]
    stop_reason: str = "stop"
    usage: dict = field(default_factory=dict)


class LLMProvider(ABC):
    @abstractmethod
    def generate(
        self,
        messages: list[Message],
        tools: list[ToolDef] | None = None,
        system: str | None = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> LLMResponse: ...

    @abstractmethod
    def supports_vision(self) -> bool: ...

    @abstractmethod
    def supports_tools(self) -> bool: ...
