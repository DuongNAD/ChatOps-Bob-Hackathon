"""
Test fixtures and shared configuration for the test suite.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock


@pytest.fixture
def mock_settings():
    """Provide mock settings for testing."""
    with patch("app.core.config.settings") as mock:
        mock.APP_NAME = "ChatOps-Bob Gateway"
        mock.APP_VERSION = "1.0.0"
        mock.DEBUG = True
        mock.HOST = "0.0.0.0"
        mock.PORT = 8000
        mock.API_V1_PREFIX = "/api/v1"
        mock.ALLOWED_ORIGINS = ["http://localhost:3000"]
        mock.WATSONX_API_URL = "https://us-south.ml.cloud.ibm.com"
        mock.WATSONX_PROJECT_ID = "test-project-id"
        mock.IBM_CLOUD_API_KEY = "test-api-key"
        mock.WATSONX_MODEL = "ibm/granite-3-8b-instruct"
        mock.TELEGRAM_BOT_TOKEN = "test-bot-token"
        mock.DATABASE_URL = "sqlite:///./data/test_chatops.db"
        mock.USE_MOCK_AI = True
        mock.FORCE_ENGLISH_OUTPUT = True
        mock.LIVA_GATEWAY_URL = "http://localhost:8082"
        yield mock


@pytest.fixture
def sample_telegram_payload():
    """Provide a sample Telegram webhook payload."""
    return {
        "update_id": 123456789,
        "message": {
            "message_id": 1,
            "from": {
                "id": 987654321,
                "is_bot": False,
                "first_name": "Test",
                "username": "testuser"
            },
            "chat": {
                "id": 987654321,
                "type": "private"
            },
            "date": 1704067200,
            "text": "Hello, ChatOps Bot!"
        }
    }
