# Second Brain Agent

An AI agent that receives messages via WhatsApp, understands your intent, and organizes/queries an Obsidian vault as your personal and professional knowledge base.

Runs 100% locally on a Windows PC. Access from anywhere via WhatsApp + Cloudflare Tunnel. Vault syncs to mobile via Obsidian + Git plugin.

## Features

- **WhatsApp interface** — send text, voice, images or PDFs, get responses
- **Obsidian vault** — notes organized in folders, with YAML frontmatter
- **Hybrid search** — BM25 keyword + vector semantic search with RRF fusion
- **Pluggable AI providers** — swap LLM/STT/Embedding just by editing `.env`
- **Auto git sync** — vault commits every 5 min, syncs to mobile via Obsidian Git
- **Vault watcher** — re-indexes notes edited manually in Obsidian

## Supported Providers

| Type | Providers |
|------|-----------|
| **LLM** | Gemini, Groq, OpenAI, Claude, OpenRouter, NVIDIA NIM |
| **STT** (voice) | Groq Whisper, OpenAI Whisper |
| **Embeddings** | Gemini, OpenAI |

## Prerequisites

- Python 3.11+
- Node.js 18+ (for Evolution API)
- [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) (for public tunnel)
- API key for at least one LLM provider

## Setup

### 1. Install dependencies

```bash
git clone https://github.com/MateusR019/Obsidian_agent.git
cd Obsidian_agent
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Configure environment

```bash
copy .env.example .env
# Edit .env with your API keys and settings
```

Mandatory variables:
- `LLM_PROVIDER` + matching API key (e.g. `NVIDIA_API_KEY`)
- `ALLOWED_NUMBERS` — your WhatsApp number as `5511999999999`
- `EVOLUTION_API_KEY` — any string, used as auth token

### 3. Initial setup (vault + database)

```bash
python scripts/setup_initial.py
```

Creates the vault folder structure and initializes SQLite. Edit `VAULT_FOLDERS` in the script to match your life before running.

### 4. Start Evolution API (WhatsApp gateway)

```bash
cd evolution-api
npm install
npm start
```

Or with Docker:
```bash
docker compose up -d
```

### 5. Connect WhatsApp

1. Open http://localhost:8080
2. Create instance `segundo-cerebro`
3. Scan QR code with WhatsApp (**Settings → Linked Devices → Link a Device**)

### 6. Start the agent

```bash
uvicorn app.main:app --reload
```

### 7. Open a public tunnel

```bash
cloudflared tunnel --url http://localhost:8000
# Copy the https://xxxx.trycloudflare.com URL
```

### 8. Configure webhook

```bash
curl -X POST http://localhost:8080/webhook/set/segundo-cerebro \
  -H "Content-Type: application/json" \
  -H "apikey: YOUR_EVOLUTION_API_KEY" \
  -d '{"url":"https://YOUR-TUNNEL-URL/webhook/whatsapp","events":["MESSAGES_UPSERT"]}'
```

### 9. Verify

```
GET http://localhost:8000/health
GET http://localhost:8000/admin   ← dashboard
```

Send a WhatsApp message and get a response!

## Switching AI Provider

Edit only `.env` — no code changes needed:

```env
# NVIDIA (default)
LLM_PROVIDER=nvidia
NVIDIA_API_KEY=your_key

# Gemini
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key

# Groq (fast + free tier)
LLM_PROVIDER=groq
GROQ_API_KEY=your_key

# Claude
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=your_key
```

## Customizing the Agent

Edit files in `vault/_SYSTEM/` (created by `setup_initial.py`):

| File | Purpose |
|------|---------|
| `regras.md` | Agent behavior rules — when to ask vs act |
| `glossario.md` | Your domain-specific terms |
| `contexto_negocio.md` | Your personal/business context |

Changes take effect on the next message.

## Vault Structure (default)

```
00_Inbox/       — unclassified notes
10_Daily/       — daily notes by year/month
20_Work/        — projects, clients, documents
30_Personal/    — finance, health, hobbies
40_Knowledge/   — articles, learnings
50_People/      — contacts
60_Archive/     — historical
_SYSTEM/        — agent config (do not commit)
```

Customize by editing `VAULT_FOLDERS` in `scripts/setup_initial.py` before first run.

## Useful Commands

```bash
# Test configured providers
python scripts/test_providers.py

# Re-index vault after bulk import
python scripts/reindex_all.py

# Start everything (Windows)
scripts\start_all.bat
```

## Troubleshooting

**Agent not responding on WhatsApp:**
- Check your number is in `ALLOWED_NUMBERS` (format: `5511999999999`)
- Verify webhook URL in Evolution API points to your tunnel
- Check server logs for each incoming message

**Vault not syncing to mobile:**
- Set `VAULT_GIT_REMOTE` in `.env` with your repo URL
- Install Obsidian Git plugin on mobile
- Configure Git credentials on the PC

**No embedding (vector search disabled):**
- Set `EMBEDDING_PROVIDER=gemini` (or openai) and add the API key
- BM25 keyword search still works without embeddings
