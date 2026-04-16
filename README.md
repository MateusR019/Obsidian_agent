# Segundo Cérebro

Agente de IA que recebe mensagens via WhatsApp, interpreta a intenção e organiza/consulta um vault Obsidian como fonte de conhecimento pessoal e profissional.

Roda 100% local no Windows. Acesso remoto via WhatsApp + Cloudflare Tunnel.

## Pré-requisitos

- Python 3.11+
- Docker Desktop
- Conta Cloudflare (para tunnel)
- API key de pelo menos um provider de IA (Gemini recomendado para início)

## Setup Passo a Passo

### 1. Clonar e instalar dependências

```bash
git clone <seu-repo>
cd segundo-cerebro
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

```bash
copy .env.example .env
# Edite .env com suas chaves de API e configurações
```

Variáveis obrigatórias no `.env`:
- `GEMINI_API_KEY` (ou chave do provider escolhido)
- `EVOLUTION_API_KEY`
- `ALLOWED_NUMBERS` — seu número no formato `5511999999999`

### 3. Setup inicial (vault + banco)

```bash
python scripts/setup_initial.py
```

Isso cria a estrutura de pastas do vault em `./vault/` e inicializa o banco SQLite.

### 4. Subir tudo

```bash
# Opção A: script Windows
scripts\start_all.bat

# Opção B: manual
docker compose up -d
uvicorn app.main:app --reload
```

### 5. Verificar saúde

```
GET http://localhost:8000/health
→ {"status": "ok", "service": "segundo-cerebro"}
```

### 6. Configurar Evolution API

1. Acesse http://localhost:8080
2. Crie uma instância chamada `segundo-cerebro`
3. Escaneie o QR code com o WhatsApp
4. Configure o webhook apontando para `https://<seu-tunnel>/webhook/whatsapp`

### 7. Cloudflare Tunnel (acesso externo)

```bash
cloudflared tunnel --url http://localhost:8000
```

Copie a URL gerada e configure como webhook na Evolution API.

## Como Trocar de Provider de IA

Edite apenas o `.env`:

```env
# Para usar Groq:
LLM_PROVIDER=groq
GROQ_API_KEY=sua_chave

# Para usar OpenAI:
LLM_PROVIDER=openai
OPENAI_API_KEY=sua_chave

# Para usar Claude:
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=sua_chave
```

Reinicie o servidor. Nenhuma mudança de código necessária.

## Como Customizar o Vault

Edite os arquivos em `vault/_SYSTEM/`:

- **`regras.md`** — comportamento do agente, quando perguntar vs agir
- **`glossario.md`** — termos do seu negócio
- **`contexto_negocio.md`** — contexto sobre suas empresas e produtos

As mudanças são aplicadas imediatamente na próxima mensagem.

## Estrutura do Vault

```
00_Inbox/           — notas não classificadas
10_Daily/           — daily notes por ano/mês
20_Operacao/        — EFish, SeaFishing, Marketplaces
30_Prime_Angling/   — operação EUA
40_Segna/           — projeto pessoal
50_Pessoal/         — saúde, finanças, hobbies
60_Pessoas/         — contatos
70_Conhecimento/    — artigos, aprendizados
80_Projetos_Ativos/ — projetos em andamento
90_Arquivo/         — histórico
_SYSTEM/            — configuração do agente (não editar estrutura)
```

## Troubleshooting

**`sqlite-vec` não carrega:**
```bash
pip install sqlite-vec --force-reinstall
```

**Evolution API não conecta:**
- Verifique se o Docker está rodando: `docker ps`
- Logs: `docker compose logs -f`

**Agente não responde no WhatsApp:**
- Confirme que o número está em `ALLOWED_NUMBERS`
- Verifique o webhook na Evolution API (deve apontar para o tunnel)
- Logs do servidor mostram cada mensagem recebida

**Vault não sincroniza no celular:**
- Configure `VAULT_GIT_REMOTE` com URL do seu repo
- Instale o plugin Git no Obsidian mobile
- Configure credenciais Git no PC

## Desenvolvimento

```bash
# Testar providers configurados
python scripts/test_providers.py

# Reindexar vault após bulk import
python scripts/reindex_all.py

# Rodar testes
pytest tests/
```
