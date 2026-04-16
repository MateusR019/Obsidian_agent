"""Sync do vault via Git (commit local + push opcional)."""
import threading
import time
from pathlib import Path
from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

_debounce_timer: threading.Timer | None = None
_debounce_lock = threading.Lock()
DEBOUNCE_SECONDS = 30


def _get_repo():
    import git
    settings = get_settings()
    vault_path = Path(settings.vault_path)
    try:
        return git.Repo(vault_path)
    except git.InvalidGitRepositoryError:
        repo = git.Repo.init(vault_path)
        logger.info(f"Git repo inicializado em {vault_path}")
        return repo


def pull() -> None:
    """Faz pull antes de escritas para evitar conflito."""
    settings = get_settings()
    if not settings.vault_git_remote:
        return
    try:
        repo = _get_repo()
        origin = repo.remotes.origin
        origin.pull()
        logger.debug("Git pull OK")
    except Exception as e:
        logger.warning(f"Git pull falhou (continuando): {e}")


def _do_commit_and_push() -> None:
    settings = get_settings()
    try:
        repo = _get_repo()
        repo.git.add(A=True)
        if not repo.is_dirty(index=True, untracked_files=True):
            return
        repo.index.commit("chore: auto-sync vault")
        logger.info("Git commit realizado")

        if settings.vault_git_remote:
            try:
                if not repo.remotes:
                    repo.create_remote("origin", settings.vault_git_remote)
                origin = repo.remotes.origin
                origin.push(settings.vault_git_branch)
                logger.info("Git push OK")
            except Exception as e:
                logger.warning(f"Git push falhou: {e}")
    except Exception as e:
        logger.error(f"Git commit falhou: {e}")


def commit_and_push(immediate: bool = False) -> None:
    """Agenda commit com debounce de 30s (ou imediato se immediate=True)."""
    global _debounce_timer
    if immediate:
        _do_commit_and_push()
        return

    with _debounce_lock:
        if _debounce_timer is not None:
            _debounce_timer.cancel()
        _debounce_timer = threading.Timer(DEBOUNCE_SECONDS, _do_commit_and_push)
        _debounce_timer.daemon = True
        _debounce_timer.start()
