# Importa todos os módulos de tools para garantir registro no registry
from app.tools import (  # noqa: F401
    vault_create,
    vault_read,
    vault_update,
    vault_search,
    vault_list,
    daily_note,
    send_message,
)