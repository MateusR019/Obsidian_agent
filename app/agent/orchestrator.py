"""Loop principal do agente: recebe mensagem → executa tools → responde."""
import json
import time
from app.config import get_settings
from app.providers.llm.base import Message
from app.providers.llm.factory import get_llm
from app.tools.registry import get_tool_defs, execute_tool
from app.tools.send_message import set_current_phone
from app.agent.prompts import build_system_prompt
from app.agent import memory as mem
from app.utils.logger import get_logger

# Garante que todas as tools estão registradas
import app.tools  # noqa: F401

logger = get_logger(__name__)

# Rate limiting simples por sessão
_rate_counters: dict[str, list[float]] = {}
RATE_LIMIT = 30  # msgs por minuto


def _check_rate_limit(session_id: str) -> bool:
    now = time.time()
    window = _rate_counters.setdefault(session_id, [])
    window[:] = [t for t in window if now - t < 60]
    if len(window) >= RATE_LIMIT:
        return False
    window.append(now)
    return True


def process_message(
    session_id: str,
    phone: str,
    text: str,
    message_id: str | None = None,
    extra_context: str | None = None,
) -> None:
    """
    Processa mensagem do usuário e envia resposta via WhatsApp.
    extra_context: conteúdo pré-processado de mídia (transcrição, OCR, etc).
    """
    settings = get_settings()

    # Deduplicação
    if message_id and mem.is_duplicate(message_id):
        logger.info(f"Mensagem duplicada ignorada: {message_id}")
        return

    # Rate limiting
    if not _check_rate_limit(session_id):
        logger.warning(f"Rate limit atingido para {session_id}")
        set_current_phone(phone)
        execute_tool("send_message", {"text": "Devagar aí! Muitas mensagens de uma vez. Espera um segundo."})
        return

    # Configura phone para send_message
    set_current_phone(phone)

    # Salva sessão e mensagem do usuário
    mem.ensure_session(session_id, phone)
    user_content = f"{extra_context}\n\n{text}".strip() if extra_context else text
    mem.save_message(session_id, "user", user_content, message_id=message_id)

    # Carrega histórico
    history = mem.get_history(session_id, window=settings.agent_history_window)

    # Loop do agente
    llm = get_llm()
    tools = get_tool_defs()
    system = build_system_prompt()
    messages = list(history)
    max_iter = settings.agent_max_tool_iterations

    for iteration in range(max_iter):
        try:
            resp = llm.generate(
                messages=messages,
                tools=tools,
                system=system,
                temperature=settings.agent_temperature,
            )
        except Exception as e:
            logger.error(f"LLM falhou na iteração {iteration}: {e}")
            execute_tool("send_message", {"text": "Poxa, tive um probleminha técnico. Tenta de novo em instantes."})
            return

        # Resposta final (sem tool calls)
        if not resp.tool_calls:
            if resp.content:
                execute_tool("send_message", {"text": resp.content})
                mem.save_message(session_id, "assistant", resp.content)
            return

        # Executa tools
        assistant_msg = Message(
            role="assistant",
            content=resp.content or "",
            tool_calls=resp.tool_calls,
        )
        messages.append(assistant_msg)
        mem.save_message(
            session_id, "assistant",
            json.dumps({"content": resp.content, "tool_calls": resp.tool_calls}),
        )

        for tc in resp.tool_calls:
            tool_name = tc["name"]
            tool_args = tc.get("arguments", {})
            logger.info(f"Executando tool: {tool_name} args={tool_args}")

            try:
                result = execute_tool(tool_name, tool_args)
                result_str = json.dumps(result, ensure_ascii=False)
            except Exception as e:
                logger.error(f"Tool {tool_name} falhou: {e}")
                result_str = json.dumps({"error": str(e)})

            tool_msg = Message(
                role="tool",
                content=result_str,
                tool_call_id=tc["id"],
            )
            messages.append(tool_msg)
            mem.save_message(
                session_id, "tool", result_str,
                tool_name=tool_name, tool_call_id=tc["id"],
            )

    # Se chegou aqui sem resposta final, pede ao LLM resumir
    logger.warning(f"Máximo de iterações atingido para sessão {session_id}")
    try:
        final = llm.generate(
            messages=messages + [Message(role="user", content="Resuma o que foi feito em uma mensagem curta.")],
            system=system,
            temperature=0.2,
        )
        if final.content:
            execute_tool("send_message", {"text": final.content})
            mem.save_message(session_id, "assistant", final.content)
    except Exception:
        execute_tool("send_message", {"text": "Pronto! Fiz o que precisava."})
