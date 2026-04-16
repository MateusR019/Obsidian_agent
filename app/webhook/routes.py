"""Webhook da Evolution API — recebe mensagens WhatsApp."""
from fastapi import APIRouter, Request, BackgroundTasks, HTTPException
from app.config import get_settings
from app.webhook.parser import parse_evolution_payload, IncomingMessage
from app.agent import memory as mem
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


def _process_incoming(msg: IncomingMessage) -> None:
    """Processa mensagem em background (pré-processa mídia e chama orchestrator)."""
    from app.agent.orchestrator import process_message
    from app.providers.llm.factory import get_llm

    session_id = msg.from_number
    phone = msg.from_number
    text = msg.text or ""
    extra_context: str | None = None

    # Pré-processa mídia
    if msg.message_type == "audio":
        from app.media.audio import transcribe_audio
        transcribed = transcribe_audio(msg.message_id)
        text = f"[Áudio transcrito]: {transcribed}"

    elif msg.message_type == "image":
        llm = get_llm()
        if llm.supports_vision():
            from app.media.image import get_image_content
            image_content = get_image_content(msg.message_id, msg.media_mime or "image/jpeg")
            # Manda como conteúdo multimodal
            caption = msg.text or "Analise esta imagem."
            extra_context = None
            # Para LLMs com vision, monta mensagem especial
            from app.agent.orchestrator import process_message as _pm
            from app.providers.llm.base import Message
            from app.agent import memory as _mem
            from app.agent.prompts import build_system_prompt
            from app.tools.registry import get_tool_defs, execute_tool
            from app.tools.send_message import set_current_phone
            from app.config import get_settings as _gs

            settings = _gs()
            set_current_phone(phone)
            _mem.ensure_session(session_id, phone)

            vision_content = image_content + [{"type": "text", "text": caption}]
            _mem.save_message(session_id, "user", str(vision_content), message_id=msg.message_id)
            history = _mem.get_history(session_id, settings.agent_history_window)

            import json
            msgs = list(history[:-1]) + [Message(role="user", content=vision_content)]
            resp = llm.generate(
                messages=msgs,
                tools=get_tool_defs(),
                system=build_system_prompt(),
                temperature=settings.agent_temperature,
            )
            if resp.content:
                execute_tool("send_message", {"text": resp.content})
                _mem.save_message(session_id, "assistant", resp.content)
            return
        else:
            text = f"[Imagem recebida] {msg.text or ''}".strip()

    elif msg.message_type == "document":
        if msg.media_mime == "application/pdf" or (msg.media_mime or "").endswith("pdf"):
            from app.media.pdf import extract_pdf_text
            pdf_text = extract_pdf_text(msg.message_id)
            extra_context = f"[Conteúdo do PDF]\n{pdf_text[:3000]}"
        else:
            text = f"[Documento recebido: {msg.media_mime}] {msg.text or ''}".strip()

    process_message(
        session_id=session_id,
        phone=phone,
        text=text,
        message_id=msg.message_id,
        extra_context=extra_context,
    )


@router.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
    settings = get_settings()

    # Valida webhook secret (opcional)
    if settings.webhook_secret:
        header_secret = request.headers.get("x-webhook-secret", "")
        if header_secret != settings.webhook_secret:
            raise HTTPException(status_code=401, detail="Unauthorized")

    payload = await request.json()
    logger.debug(f"Webhook recebido: event={payload.get('event')}")

    msg = parse_evolution_payload(payload)
    if msg is None:
        return {"ok": True, "skipped": True}

    # Autorização por número
    allowed = settings.allowed_numbers_list
    if allowed and msg.from_number not in allowed:
        logger.warning(f"Número não autorizado: {msg.from_number}")
        return {"ok": True, "skipped": True}

    # Deduplicação rápida antes de enfileirar
    if msg.message_id and mem.is_duplicate(msg.message_id):
        logger.info(f"Webhook duplicado ignorado: {msg.message_id}")
        return {"ok": True, "skipped": True}

    # Processa em background — retorna 200 imediato pro Evolution
    background_tasks.add_task(_process_incoming, msg)
    return {"ok": True}
