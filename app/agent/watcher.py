"""Watcher de filesystem: re-indexa notas editadas manualmente no Obsidian."""
import threading
from pathlib import Path
from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
_observer = None


def _get_vault_path() -> Path:
    return Path(get_settings().vault_path).resolve()


class _VaultHandler:
    def __init__(self):
        self._pending: set[str] = set()
        self._lock = threading.Lock()
        self._timer: threading.Timer | None = None

    def dispatch(self, event) -> None:
        if event.is_directory:
            return
        src = getattr(event, "src_path", "")
        if not src.endswith(".md"):
            return
        if "_SYSTEM" in src:
            return
        with self._lock:
            self._pending.add(src)
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(5.0, self._flush)
            self._timer.daemon = True
            self._timer.start()

    def _flush(self) -> None:
        with self._lock:
            paths = list(self._pending)
            self._pending.clear()

        vault = _get_vault_path()
        from app.indexer.indexer import index_note
        for p in paths:
            try:
                rel = str(Path(p).relative_to(vault)).replace("\\", "/")
                count = index_note(rel)
                logger.info(f"Re-indexado (watcher): {rel} — {count} chunks")
            except Exception as e:
                logger.error(f"Watcher re-index falhou para {p}: {e}")


def start_watcher() -> None:
    """Inicia watcher do vault em thread separada."""
    global _observer
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        vault = _get_vault_path()
        handler = _VaultHandler()

        class _WD(FileSystemEventHandler):
            def on_modified(self, event):
                handler.dispatch(event)
            def on_created(self, event):
                handler.dispatch(event)

        _observer = Observer()
        _observer.schedule(_WD(), str(vault), recursive=True)
        _observer.daemon = True
        _observer.start()
        logger.info(f"Vault watcher iniciado em {vault}")
    except Exception as e:
        logger.warning(f"Vault watcher não iniciado: {e}")


def stop_watcher() -> None:
    global _observer
    if _observer:
        _observer.stop()
        _observer = None
