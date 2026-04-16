"""Provider Anthropic Claude."""
import json
import httpx
from app.providers.llm.base import LLMProvider, Message, ToolDef, LLMResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)

ANTHROPIC_BASE = "https://api.anthropic.com/v1"
DEFAULT_MODEL = "claude-sonnet-4-6"
ANTHROPIC_VERSION = "2023-06-01"


class ClaudeLLM(LLMProvider):
    def __init__(self, api_key: str, model: str = ""):
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY não configurada")
        self._api_key = api_key
        self._model = model or DEFAULT_MODEL

    def _convert_messages(self, messages: list[Message]) -> list[dict]:
        result: list[dict] = []
        for msg in messages:
            if msg.role == "system":
                continue
            if msg.role == "tool":
                result.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": msg.tool_call_id or "",
                        "content": msg.content if isinstance(msg.content, str) else json.dumps(msg.content),
                    }],
                })
            elif msg.role == "assistant" and msg.tool_calls:
                parts: list[dict] = []
                if msg.content:
                    parts.append({"type": "text", "text": msg.content})
                for tc in msg.tool_calls:
                    parts.append({
                        "type": "tool_use",
                        "id": tc["id"],
                        "name": tc["name"],
                        "input": tc.get("arguments", {}),
                    })
                result.append({"role": "assistant", "content": parts})
            else:
                content_val = msg.content
                if isinstance(content_val, list):
                    result.append({"role": msg.role, "content": content_val})
                else:
                    result.append({"role": msg.role, "content": content_val})
        return result

    def generate(
        self,
        messages: list[Message],
        tools: list[ToolDef] | None = None,
        system: str | None = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> LLMResponse:
        payload: dict = {
            "model": self._model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": self._convert_messages(messages),
        }
        if system:
            payload["system"] = system
        if tools:
            payload["tools"] = [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.parameters,
                }
                for t in tools
            ]

        resp = httpx.post(
            f"{ANTHROPIC_BASE}/messages",
            json=payload,
            headers={
                "x-api-key": self._api_key,
                "anthropic-version": ANTHROPIC_VERSION,
                "content-type": "application/json",
            },
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()

        text_out: str | None = None
        tool_calls: list[dict] = []

        for block in data.get("content", []):
            if block["type"] == "text":
                text_out = (text_out or "") + block["text"]
            elif block["type"] == "tool_use":
                tool_calls.append({
                    "id": block["id"],
                    "name": block["name"],
                    "arguments": block.get("input", {}),
                })

        usage = data.get("usage", {})
        return LLMResponse(
            content=text_out,
            tool_calls=tool_calls,
            stop_reason=data.get("stop_reason", "stop"),
            usage={
                "input_tokens": usage.get("input_tokens", 0),
                "output_tokens": usage.get("output_tokens", 0),
            },
        )

    def supports_vision(self) -> bool:
        return True

    def supports_tools(self) -> bool:
        return True
