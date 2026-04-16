"""Definições de schema das tabelas SQLite."""

SCHEMA_MESSAGES = """
CREATE TABLE IF NOT EXISTS messages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  TEXT NOT NULL,
    message_id  TEXT UNIQUE,
    role        TEXT NOT NULL CHECK(role IN ('user','assistant','tool')),
    content     TEXT NOT NULL,
    tool_name   TEXT,
    tool_call_id TEXT,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id, created_at);
CREATE INDEX IF NOT EXISTS idx_messages_msgid  ON messages(message_id);
"""

SCHEMA_SESSIONS = """
CREATE TABLE IF NOT EXISTS sessions (
    id          TEXT PRIMARY KEY,
    phone       TEXT NOT NULL,
    last_seen   TEXT NOT NULL DEFAULT (datetime('now')),
    meta        TEXT DEFAULT '{}'
);
"""

SCHEMA_VAULT_FILES = """
CREATE TABLE IF NOT EXISTS vault_files (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    path        TEXT UNIQUE NOT NULL,
    title       TEXT,
    tipo        TEXT,
    area        TEXT,
    tags        TEXT,
    mtime       REAL,
    indexed_at  TEXT
);
CREATE INDEX IF NOT EXISTS idx_vault_files_path ON vault_files(path);
CREATE INDEX IF NOT EXISTS idx_vault_files_area ON vault_files(area);
"""

SCHEMA_VEC_CHUNKS = """
CREATE TABLE IF NOT EXISTS vec_chunks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id     INTEGER NOT NULL REFERENCES vault_files(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    chunk_text  TEXT NOT NULL,
    embedding   BLOB
);
CREATE INDEX IF NOT EXISTS idx_vec_chunks_file ON vec_chunks(file_id);
"""
