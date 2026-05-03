# ChatOps-Bob Gateway

> **IBM Bob Dev Day Hackathon** — A ChatOps microservice that bridges Telegram with IBM Bob AI via RPA automation, powered by IBM Watsonx Granite.

## 🎯 What It Does

Send a `/bob` command from Telegram → the gateway automates VS Code's Bob IDE via RPA (pyautogui) → Bob executes the task → screenshot + code result sent back to Telegram.

```
Telegram  →  FastAPI Webhook  →  Message Router  →  IBM Watsonx AI / Bob RPA
   ↑                                                        ↓
   └──────────────  Screenshot + Code Result  ←─────────────┘
```

## 🏗️ Architecture

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **API Gateway** | FastAPI (async) | Webhook handlers, REST API, Dashboard |
| **AI Engine** | IBM Watsonx `ibm/granite-3-8b-instruct` | Natural language processing |
| **Chat Platform** | Telegram Bot (webhook) | User interface via mobile/desktop |
| **RPA Automation** | pyautogui + pixel detection | Automate Bob IDE in VS Code |
| **Database** | SQLite (async via aiosqlite) | Conversation history & sessions |
| **MCP Server** | `chatops-gateway` (4 tools) | External AI tool integration |
| **Dashboard** | HTML/CSS/JS | Real-time monitoring UI |

## 📁 Project Structure

```
ChatOps-Bob-Hackathon/
├── app/
│   ├── api/v1/endpoints/
│   │   ├── webhook.py           # Telegram webhook + bot commands
│   │   └── dashboard.py         # REST API: conversations & stats
│   ├── core/config.py           # Pydantic settings
│   ├── models/conversation.py   # Async SQLite database layer
│   ├── schemas/message.py       # Pydantic V2 message schemas
│   ├── services/
│   │   ├── channel_adapters/
│   │   │   └── telegram.py      # Telegram Bot adapter
│   │   ├── ibm_ai_client.py     # IBM Watsonx AI client (mock + live)
│   │   ├── message_router.py    # Message routing + /bob handler
│   │   └── rpa_controller.py    # Bob IDE RPA automation
│   ├── mcp/server.py            # MCP server (4 tools)
│   ├── static/                  # Dashboard assets (CSS, JS)
│   └── templates/               # Dashboard HTML
├── bob_sessions/                # Bob IDE task histories + screenshots
├── data/
│   ├── chatops.db               # SQLite database (auto-created)
│   └── screenshots/             # RPA-captured screenshots
├── tests/                       # Pytest test suite
├── main.py                      # App entry point + dashboard route
└── requirements.txt
```

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- IBM Bob IDE extension in VS Code
- Telegram Bot token (via [@BotFather](https://t.me/BotFather))
- IBM Cloud API key (for Watsonx AI)
- ngrok (for Telegram webhook tunneling)

### Setup

```bash
# 1. Clone & enter project
git clone https://github.com/DuongNAD/ChatOps-Bob-Hackathon.git
cd ChatOps-Bob-Hackathon

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1        # Windows PowerShell

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env
# Edit .env with your real API keys

# 5. Start the server
python -m uvicorn main:app --reload

# 6. Open dashboard
# Visit http://localhost:8000/dashboard

# 7. Expose via ngrok (new terminal)
ngrok http 8000

# 8. Set Telegram webhook
# POST https://api.telegram.org/bot<TOKEN>/setWebhook?url=<NGROK_URL>/api/v1/webhook/telegram
```

### 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/status` | Check system status (AI mode, DB, connections) |
| `/history` | View your recent conversation history |
| `/bob <task>` | Send a task to IBM Bob AI in VS Code |
| *(any text)* | Chat directly with IBM Granite AI |

### 📡 REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | System health check |
| `GET` | `/dashboard` | Web monitoring dashboard |
| `GET` | `/api/v1/conversations` | Recent conversations |
| `GET` | `/api/v1/stats` | System statistics |
| `POST` | `/api/v1/webhook/telegram` | Telegram webhook |
| `GET` | `/docs` | OpenAPI documentation |

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `IBM_CLOUD_API_KEY` | IBM Cloud API key for Watsonx |
| `WATSONX_PROJECT_ID` | Watsonx project ID |
| `WATSONX_MODEL` | AI model (default: `ibm/granite-3-8b-instruct`) |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot API token |
| `USE_MOCK_AI` | `True` for mock responses, `False` for real AI |
| `DATABASE_URL` | SQLite database URL |

## 🧪 Testing

```bash
pytest                              # Run all tests
pytest --cov=app --cov-report=html  # With coverage report
pytest tests/test_chatops.py -v     # Run specific test file
```

## 🔧 MCP Server

The gateway includes an MCP (Model Context Protocol) server with 4 tools:

| Tool | Description |
|------|-------------|
| `fetch_recent_conversations` | Get 5 most recent user messages |
| `search_conversations` | Search messages by keyword |
| `get_session_stats` | Session counts, message breakdowns |
| `get_system_health` | Database, screenshots, system status |

Run standalone: `python -m app.mcp.server`

## 📸 Bob Sessions & Evidence

See [`bob_sessions/`](bob_sessions/) for:
- **20 task sessions** documenting the full development flow
- **23 screenshots** from Bob IDE showing real task execution
- **Bobcoin consumption**: 27.15 / 40.00 used (68%)

## 👤 Author

**Dương Nguyễn Anh** — duonganhdn2000@gmail.com

Team: `DuongAnh` | Plan: Enterprise

---

*Built with IBM Bob IDE & IBM Watsonx AI for the IBM Bob Dev Day Hackathon 2026*