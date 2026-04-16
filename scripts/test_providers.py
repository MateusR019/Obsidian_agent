"""Testa providers configurados no .env e reporta status."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger("test_providers")


def test_llm() -> bool:
    from app.providers.llm.factory import get_llm
    from app.providers.llm.base import Message

    settings = get_settings()
    logger.info(f"Testando LLM provider: {settings.llm_provider}")
    try:
        llm = get_llm()
        resp = llm.generate(
            messages=[Message(role="user", content="Responda apenas: OK")],
            max_tokens=10,
        )
        logger.info(f"LLM OK — resposta: {repr(resp.content)} | uso: {resp.usage}")
        return True
    except Exception as e:
        logger.error(f"LLM FALHOU: {e}")
        return False


def test_embedding() -> bool:
    from app.providers.embed.factory import get_embedding

    settings = get_settings()
    logger.info(f"Testando Embedding provider: {settings.embedding_provider}")
    try:
        emb = get_embedding()
        vecs = emb.embed(["teste de embedding"])
        assert len(vecs) == 1
        assert len(vecs[0]) > 0
        logger.info(f"Embedding OK — dimensão: {len(vecs[0])}")
        return True
    except Exception as e:
        logger.error(f"Embedding FALHOU: {e}")
        return False


def test_stt() -> bool:
    settings = get_settings()
    logger.info(f"Testando STT provider: {settings.stt_provider} (sem áudio real — só instanciação)")
    try:
        from app.providers.stt.factory import get_stt
        get_stt()
        logger.info("STT OK — instância criada")
        return True
    except NotImplementedError as e:
        logger.warning(f"STT não implementado: {e}")
        return False
    except Exception as e:
        logger.error(f"STT FALHOU: {e}")
        return False


def main() -> None:
    results: dict[str, bool] = {}
    results["LLM"] = test_llm()
    results["Embedding"] = test_embedding()
    results["STT"] = test_stt()

    print("\n=== Resultado dos Providers ===")
    for name, ok in results.items():
        status = "[OK]" if ok else "[FALHOU]"
        print(f"  {name:12} {status}")

    if not all(results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
