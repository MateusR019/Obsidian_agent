"""Divide notas markdown em chunks respeitando headers como fronteiras."""
import re

CHUNK_SIZE = 500    # tokens aproximados (chars / 4)
CHUNK_OVERLAP = 50


def _approx_tokens(text: str) -> int:
    return len(text) // 4


def chunk_markdown(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Divide texto em chunks de ~chunk_size tokens com overlap.
    Usa headers markdown como fronteiras naturais.
    """
    # Separa em seções por header
    sections = re.split(r"(?=^#{1,6} )", text, flags=re.MULTILINE)
    sections = [s.strip() for s in sections if s.strip()]

    chunks: list[str] = []
    current = ""

    for section in sections:
        if _approx_tokens(current + "\n\n" + section) <= chunk_size:
            current = (current + "\n\n" + section).strip() if current else section
        else:
            if current:
                chunks.append(current)
            # Se a seção sozinha ainda é grande, divide por parágrafo
            if _approx_tokens(section) > chunk_size:
                paragraphs = re.split(r"\n{2,}", section)
                buf = ""
                for para in paragraphs:
                    if _approx_tokens(buf + "\n\n" + para) <= chunk_size:
                        buf = (buf + "\n\n" + para).strip() if buf else para
                    else:
                        if buf:
                            chunks.append(buf)
                        buf = para
                if buf:
                    current = buf
                else:
                    current = ""
            else:
                current = section

    if current:
        chunks.append(current)

    # Aplica overlap: cada chunk reaproveita final do anterior
    if overlap > 0 and len(chunks) > 1:
        overlapped: list[str] = [chunks[0]]
        for i in range(1, len(chunks)):
            prev_tail = chunks[i - 1][-overlap * 4:]  # ~overlap tokens
            overlapped.append(prev_tail + "\n" + chunks[i])
        return overlapped

    return chunks
