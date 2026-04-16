"""Provider Gemini via REST API (google.generativeai não necessário)."""
import json
import uuid
import httpx
from app.providers.llm.base import LLMProvider, Message, ToolDef, LLMResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)

GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
DEFAULT_MODEL = "gemini-2.0-flash"


class GeminiLLM(LLMProvider):
    def __init__(self, api_key: str, model: str = ""):
        if not api_key:
            raise ValueError("GEMINI_API_KEY não configurada")
        self._api_key = api_key
        self._model = model or DEFAULT_MODEL

    def generate(
        self,
        messages: list[Message],
        tools: list[ToolDef] | None = None,
        system: str | None = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> LLMResponse:
        url = f"{GEMINI_BASE}/{self._model}:generateContent?key={self._api_key}"

        contents = []
        for msg in messages:
            if msg.role == "system":
                continue  # handled via systemInstruction
            if msg.role == "tool":
                contents.append({
                    "role": "user",
                    "parts": [{"functionResponse": {
                        "name": msg.tool_call_id or "tool",
                        "response": {"output": msg.content},
                    }}],
                })
            elif msg.role == "assistant":
                parts: list[dict] = []
                if msg.content:
                    parts.append({"text": msg.content})
                if msg.tool_calls:
                    for tc in msg.tool_calls:
                        parts.append({"functionCall": {
                            "name": tc["name"],
                            "args": tc.get("arguments", {}),
                        }})
                contents.append({"role": "model", "parts": parts})
            else:
                content_val = msg.content
                if isinstance(content_val, list):
                    parts = content_val
                else:
                    parts = [{"text": content_val}]
                contents.append({"role": "user", "parts": parts})

        payload: dict = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
        }

        # System instruction
        system_text = system or ""
        if system_text:
            payload["systemInstruction"] = {"parts": [{"text": system_text}]}

        # Tools
        if tools:
            payload["tools"] = [{"functionDeclarations": [
                {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.parameters,
                }
                for t in tools
            ]}]
            payload["toolConfig"] = {"functionCallingConfig": {"mode": "AUTO"}}

        resp = httpx.post(url, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        candidate = data["candidates"][0]
        content_part = candidate.get("content", {})
        parts = content_part.get("parts", [])

        text_out: str | None = None
        tool_calls: list[dict] = []

        for part in parts:
            if "text" in part:
                text_out = (text_out or "") + part["text"]
            if "functionCall" in part:
                fc = part["functionCall"]
                tool_calls.append({
                    "id": str(uuid.uuid4()),
                    "name": fc["name"],
                    "arguments": fc.get("args", {}),
                })

        usage = data.get("usageMetadata", {})
        stop_reason = candidate.get("finishReason", "stop").lower()

        return LLMResponse(
            content=text_out,
            tool_calls=tool_calls,
            stop_reason=stop_reason,
            usage={
                "input_tokens": usage.get("promptTokenCount", 0),
                "output_tokens": usage.get("candidatesTokenCount", 0),
            },
        )

    def supports_vision(self) -> bool:
        return True

    def supports_tools(self) -> bool:
        return True
