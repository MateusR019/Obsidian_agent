"""Normaliza payload da Evolution API para formato interno."""
from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass
class IncomingMessage:
    from_number: str
    message_type: Literal["text", "audio", "image", "document"]
    text: str | None
    media_url: str | None
    media_mime: str | None
    timestamp: datetime
    message_id: str


def parse_evolution_payload(payload: dict) -> IncomingMessage | None:
    """
    Parseia payload do webhook Evolution API.
    Retorna None se não for mensagem de usuário (ex: status, ack, etc).
    """
    event = payload.get("event", "")
    if event not in ("messages.upsert", "messages.update"):
        return None

    data = payload.get("data", {})
    key = data.get("key", {})
    message = data.get("message", {})

    # Ignora mensagens enviadas pelo próprio bot
    if key.get("fromMe", False):
        return None

    # Ignora atualizações de status
    if payload.get("event") == "messages.update":
        return None

    from_number = key.get("remoteJid", "").replace("@s.whatsapp.net", "").replace("@g.us", "")
    message_id = key.get("id", "")
    timestamp_raw = data.get("messageTimestamp", 0)
    timestamp = datetime.fromtimestamp(int(timestamp_raw)) if timestamp_raw else datetime.now()

    # Detecta tipo de mensagem
    if "conversation" in message or "extendedTextMessage" in message:
        text = message.get("conversation") or message.get("extendedTextMessage", {}).get("text", "")
        return IncomingMessage(
            from_number=from_number,
            message_type="text",
            text=text,
            media_url=None,
            media_mime=None,
            timestamp=timestamp,
            message_id=message_id,
        )

    if "audioMessage" in message:
        audio = message["audioMessage"]
        return IncomingMessage(
            from_number=from_number,
            message_type="audio",
            text=None,
            media_url=None,
            media_mime=audio.get("mimetype", "audio/ogg"),
            timestamp=timestamp,
            message_id=message_id,
        )

    if "imageMessage" in message:
        img = message["imageMessage"]
        return IncomingMessage(
            from_number=from_number,
            message_type="image",
            text=img.get("caption"),
            media_url=None,
            media_mime=img.get("mimetype", "image/jpeg"),
            timestamp=timestamp,
            message_id=message_id,
        )

    if "documentMessage" in message or "documentWithCaptionMessage" in message:
        doc = message.get("documentMessage") or message.get("documentWithCaptionMessage", {}).get("message", {}).get("documentMessage", {})
        return IncomingMessage(
            from_number=from_number,
            message_type="document",
            text=doc.get("caption"),
            media_url=None,
            media_mime=doc.get("mimetype", "application/octet-stream"),
            timestamp=timestamp,
            message_id=message_id,
        )

    return None
