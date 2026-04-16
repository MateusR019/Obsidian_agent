from abc import ABC, abstractmethod


class STTProvider(ABC):
    @abstractmethod
    def transcribe(self, audio_bytes: bytes, mime_type: str = "audio/ogg") -> str:
        """Transcreve áudio para texto em PT-BR."""
        ...
