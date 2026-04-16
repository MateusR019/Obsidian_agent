"""Provider Groq — API compatível com OpenAI."""
import json
import httpx
from app.providers.llm.base import LLMProvider, Message, ToolDef, LLMResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)

GROQ_BASE = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "llama-3.3-70b-versatile"


class GroqLLM(LLMProvider):
    def __init__(self, api_key: str, model: str = ""):
        if not api_key:
            raise ValueError("GROQ_API_KEY não configurada")
        self._api_key = api_key
        self._model = model or DEFAULT_MODEL

    def _convert_messages(self, messages: list[Message], system: str | None) -> list[dict]:
        result: list[dict] = []
        if system:
            result.append({"role": "system", "content": system})
        for msg in messages:
            if msg.role == "system":
                continue
            if msg.role == "tool":
                result.append({
                    "role": "tool",
                    "tool_call_id": msg.tool_call_id or "",
                    "content": msg.content if isinstance(msg.content, str) else json.dumps(msg.content),
                })
            elif msg.role == "assistant" and msg.tool_calls:
                result.append({
                    "role": "assistant",
                    "content": msg.content or None,
                    "tool_calls": [
                        {
                            "id": tc["id"],
                            "type": "function",
                            "function": {
                                "name": tc["name"],
                                "arguments": json.dumps(tc.get("arguments", {})),
                            },
                        }
                        for tc in msg.tool_calls
                    ],
                })
            else:
                result.append({
                    "role": msg.role,
                    "content": msg.content if isinstance(msg.content, str) else json.dumps(msg.content),
                })
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
            "messages": self._convert_messages(messages, system),
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if tools:
            payload["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.parameters,
                    },
                }
                for t in tools
            ]
            payload["tool_choice"] = "auto"

        resp = httpx.post(
            f"{GROQ_BASE}/chat/completions",
            json=payload,
            headers={"Authorization": f"Bearer {self._api_key}"},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()

        choice = data["choices"][0]
        msg = choice["message"]
        text_out = msg.get("content")
        raw_tcs = msg.get("tool_calls") or []
        tool_calls = [
            {
                "id": tc["id"],
                "name": tc["function"]["name"],
                "arguments": json.loads(tc["function"]["arguments"] or "{}"),
            }
            for tc in raw_tcs
        ]
        usage = data.get("usage", {})
        return LLMResponse(
            content=text_out,
            tool_calls=tool_calls,
            stop_reason=choice.get("finish_reason", "stop"),
            usage={
                "input_tokens": usage.get("prompt_tokens", 0),
                "output_tokens": usage.get("completion_tokens", 0),
            },
        )

    def supports_vision(self) -> bool:
        return False

    def supports_tools(self) -> bool:
        return True
