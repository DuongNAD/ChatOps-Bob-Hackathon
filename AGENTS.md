# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project: ChatOps-Bob Gateway
FastAPI microservice for IBM Bob Dev Day Hackathon - transforms into a ChatOps gateway with Telegram Bot integration and IBM Watsonx AI.

## Critical Architecture Rules

### Database Storage
- **CRITICAL**: SQLite database MUST be stored at `data/chatops.db` (NOT in `bob_sessions/`)
- Use async SQLite only (aiosqlite or sqlalchemy async)
- `bob_sessions/` is for Bob agent sessions, NEVER for application data

### AI Engine
- Use `ibm-watsonx-ai` SDK with model `ibm/granite-3-8b-instruct`
- All AI interactions must be async

### Social Integration
- Telegram Bot via webhook (not polling)
- All webhook handlers must be async

### Code Patterns
- **CRITICAL**: ALL I/O operations MUST be async (no sync database/file/network calls)
- Use Pydantic V2 for all schemas (already installed)
- FastAPI async endpoints only

## Test Commands
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run single test file
pytest tests/test_scan.py

# Run specific test
pytest tests/test_scan.py::test_function_name
```

## Current State
- Existing `app/api/v1/endpoints/scan.py` and `app/schemas/scan.py` are placeholder code - will be replaced
- 27 existing tests are for old code - will be replaced with new ChatOps tests
- Virtual environment: Python 3.13 in `venv/`
- Config uses pydantic-settings (already set up in `app/core/config.py`)

## Non-Obvious Gotchas
- Windows PowerShell: Use `.\venv\Scripts\Activate.ps1` to activate venv
- pytest.ini has `asyncio_mode = auto` - async tests work automatically
- CORS already configured in main.py for localhost:3000 and localhost:8000