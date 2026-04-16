"""Dashboard /admin com métricas básicas."""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.db.connection import get_connection
from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
admin_router = APIRouter()

_HTML = """\
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Segundo Cérebro — Admin</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 16px; color: #1a1a1a; }}
    h1 {{ font-size: 1.5rem; border-bottom: 2px solid #4f46e5; padding-bottom: 8px; }}
    .card {{ background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; margin: 12px 0; }}
    .card h2 {{ margin: 0 0 8px; font-size: 1rem; color: #4f46e5; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.875rem; }}
    th {{ text-align: left; padding: 6px; background: #e5e7eb; }}
    td {{ padding: 6px; border-bottom: 1px solid #f3f4f6; }}
    .badge {{ display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 0.75rem; background: #dbeafe; color: #1e40af; }}
    .ok {{ background: #dcfce7; color: #166534; }}
    a {{ color: #4f46e5; text-decoration: none; }}
  </style>
</head>
<body>
  <h1>Segundo Cérebro — Admin</h1>

  <div class="card">
    <h2>Status</h2>
    <table>
      <tr><th>Provider LLM</th><td><span class="badge ok">{llm_provider}</span> {llm_model}</td></tr>
      <tr><th>Provider STT</th><td><span class="badge">{stt_provider}</span></td></tr>
      <tr><th>Provider Embed</th><td><span class="badge">{embed_provider}</span></td></tr>
      <tr><th>Vault Path</th><td>{vault_path}</td></tr>
    </table>
  </div>

  <div class="card">
    <h2>Vault</h2>
    <table>
      <tr><th>Total de notas indexadas</th><td>{vault_notes}</td></tr>
      <tr><th>Total de chunks</th><td>{vault_chunks}</td></tr>
    </table>
    <br>
    <table>
      <tr><th>Área</th><th>Notas</th></tr>
      {area_rows}
    </table>
  </div>

  <div class="card">
    <h2>Últimas Mensagens</h2>
    <table>
      <tr><th>Quando</th><th>Sessão</th><th>Role</th><th>Conteúdo</th></tr>
      {message_rows}
    </table>
  </div>

  <p style="color:#9ca3af;font-size:0.75rem">Atualiza ao recarregar · <a href="/health">health</a> · <a href="/docs">API docs</a></p>
</body>
</html>
"""


@admin_router.get("/admin", response_class=HTMLResponse)
def admin_dashboard():
    settings = get_settings()
    conn = get_connection()

    vault_notes = conn.execute("SELECT COUNT(*) FROM vault_files").fetchone()[0]
    vault_chunks = conn.execute("SELECT COUNT(*) FROM vec_chunks").fetchone()[0]

    area_rows_data = conn.execute(
        "SELECT area, COUNT(*) as c FROM vault_files WHERE area != '' GROUP BY area ORDER BY c DESC LIMIT 10"
    ).fetchall()
    area_rows = "".join(f"<tr><td>{r['area']}</td><td>{r['c']}</td></tr>" for r in area_rows_data)
    if not area_rows:
        area_rows = "<tr><td colspan='2'>Nenhuma nota indexada ainda</td></tr>"

    msgs = conn.execute(
        "SELECT created_at, session_id, role, content FROM messages ORDER BY created_at DESC LIMIT 20"
    ).fetchall()
    message_rows = "".join(
        f"<tr><td style='white-space:nowrap'>{r['created_at'][:16]}</td>"
        f"<td>{r['session_id'][-6:]}</td>"
        f"<td><span class='badge'>{r['role']}</span></td>"
        f"<td>{str(r['content'])[:80].replace('<','&lt;')}</td></tr>"
        for r in msgs
    )
    if not message_rows:
        message_rows = "<tr><td colspan='4'>Nenhuma mensagem ainda</td></tr>"

    html = _HTML.format(
        llm_provider=settings.llm_provider,
        llm_model=settings.llm_model or "default",
        stt_provider=settings.stt_provider,
        embed_provider=settings.embedding_provider,
        vault_path=settings.vault_path,
        vault_notes=vault_notes,
        vault_chunks=vault_chunks,
        area_rows=area_rows,
        message_rows=message_rows,
    )
    return HTMLResponse(content=html)


@admin_router.get("/admin/stats")
def admin_stats():
    conn = get_connection()
    return {
        "vault_notes": conn.execute("SELECT COUNT(*) FROM vault_files").fetchone()[0],
        "vault_chunks": conn.execute("SELECT COUNT(*) FROM vec_chunks").fetchone()[0],
        "messages_total": conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0],
        "sessions": conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0],
        "errors_recent": 0,
    }
