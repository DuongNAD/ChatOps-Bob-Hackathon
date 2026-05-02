# ChatOps-Bob Gateway

> **IBM Bob Dev Day Hackathon** — A ChatOps microservice that bridges Telegram with IBM Bob AI via RPA automation.

## 🎯 What It Does

Send a `/bob` command from Telegram → the gateway automates VS Code's Bob IDE via RPA (pyautogui) → Bob executes the task → screenshot + code result sent back to Telegram.

```
Telegram  →  FastAPI Webhook  →  RPA Controller  →  Bob IDE (VS Code)
   ↑                                                       ↓
   └──────────────  Screenshot + Code Result  ←────────────┘
```

## 🏗️ Architecture

| Layer | Technology |
|-------|-----------|
| **API Framework** | FastAPI (async) |
| **AI Engine** | IBM Watsonx `ibm/granite-3-8b-instruct` |
| **Chat Platform** | Telegram Bot (webhook) |
| **RPA Automation** | pyautogui + pygetwindow + Pillow |
| **Database** | SQLite (async via aiosqlite) |
| **MCP Server** | `chatops-gateway` for conversation queries |

## 📁 Project Structure

```
IBM_Hackathon/
├── app/
│   ├── api/v1/endpoints/
│   │   ├── scan.py              # Legacy scan endpoint
│   │   └── webhook.py           # Telegram webhook handler
│   ├── core/config.py           # Pydantic settings
│   ├── models/conversation.py   # SQLite async database layer
│   ├── schemas/message.py       # Pydantic V2 schemas
│   ├── services/
│   │   ├── channel_adapters/
│   │   │   └── telegram.py      # Telegram Bot adapter
│   │   ├── ibm_ai_client.py     # IBM Watsonx AI client
│   │   ├── message_router.py    # Message routing + /bob handler
│   │   └── rpa_controller.py    # Bob IDE RPA automation
│   └── mcp/server.py            # MCP server for conversations
├── bob_sessions/                # Bob IDE task histories + screenshots
├── data/
│   ├── chatops.db               # SQLite database (auto-created)
│   └── screenshots/             # RPA-captured screenshots
├── tests/
├── AGENTS.md                    # AI coding rules
├── main.py                      # App entry point
└── requirements.txt
```

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- IBM Bob IDE extension in VS Code
- Telegram Bot token
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
.\venv\Scripts\python.exe -m uvicorn main:app --reload

# 6. Expose via ngrok (new terminal)
ngrok http 8000

# 7. Set Telegram webhook
# POST https://api.telegram.org/bot<TOKEN>/setWebhook?url=<NGROK_URL>/api/v1/webhook/telegram
```

### Usage

In Telegram, send to your bot:
- **Chat with AI**: Just type any message → IBM Granite AI responds
- **Run Bob IDE task**: `/bob Write a Python function to calculate Fibonacci series`
- **Get weather**: `/bob Write a Python script that fetches Tokyo weather`

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `IBM_CLOUD_API_KEY` | IBM Cloud API key for Watsonx |
| `WATSONX_PROJECT_ID` | Watsonx project ID |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot API token |
| `USE_MOCK_AI` | `True` for mock responses, `False` for real AI |
| `FORCE_ENGLISH_OUTPUT` | Force AI to respond in English |

## 🧪 Testing

```bash
pytest                              # Run all tests
pytest --cov=app --cov-report=html  # With coverage
```

## 📸 Bob Sessions & Evidence

See [`bob_sessions/`](bob_sessions/) for:
- **20 task sessions** documenting the full development flow
- **23 screenshots** from Bob IDE showing real task execution
- **Bobcoin consumption**: 27.15 / 40.00 used (68%)

## 👤 Author

**Dương Nguyễn Anh** — duonganhdn2000@gmail.com

Team: `DuongAnh` | Plan: Enterprise

---

*Built with IBM Bob IDE for the IBM Bob Dev Day Hackathon*