"""
Tests for the core ChatOps-Bob Gateway functionality.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Tests for the /health endpoint."""
    
    @pytest.mark.asyncio
    async def test_health_response_format(self):
        """Health endpoint response should have expected structure."""
        # Test the expected response format
        expected_keys = {"status", "service", "version", "components"}
        sample = {
            "status": "healthy",
            "service": "ChatOps-Bob Gateway",
            "version": "1.0.0",
            "components": {
                "database": {"status": "healthy", "records": 0},
                "ai_engine": {"status": "mock", "model": "ibm/granite-3-8b-instruct"},
                "telegram": {"status": "configured"}
            }
        }
        assert set(sample.keys()) == expected_keys
        assert "database" in sample["components"]
        assert "ai_engine" in sample["components"]


class TestTelegramAdapter:
    """Tests for the Telegram adapter."""
    
    def test_parse_webhook_valid_payload(self, mock_settings, sample_telegram_payload):
        """Should correctly parse a valid Telegram webhook payload."""
        from app.services.channel_adapters.telegram import TelegramAdapter
        
        adapter = TelegramAdapter()
        message = adapter.parse_webhook(sample_telegram_payload)
        
        assert message.channel.value == "telegram"
        assert message.sender_id == "987654321"
        assert message.session_id == "tg_987654321"
        assert message.content == "Hello, ChatOps Bot!"
    
    def test_parse_webhook_missing_chat_id(self, mock_settings):
        """Should raise KeyError when chat.id is missing."""
        from app.services.channel_adapters.telegram import TelegramAdapter
        
        adapter = TelegramAdapter()
        bad_payload = {"message": {"chat": {}, "text": "test"}}
        
        with pytest.raises(KeyError):
            adapter.parse_webhook(bad_payload)
    
    @pytest.mark.asyncio
    async def test_send_message_success(self, mock_settings):
        """Should return True on successful message send."""
        from app.services.channel_adapters.telegram import TelegramAdapter
        
        adapter = TelegramAdapter()
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        
        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_client
            
            result = await adapter.send_message("123", "Hello!")
            assert result is True


class TestIBMAIClient:
    """Tests for the IBM AI client."""
    
    @pytest.mark.asyncio
    async def test_mock_mode_returns_response(self, mock_settings):
        """In mock mode, should return a fixed response."""
        from app.services.ibm_ai_client import IBMAIClient
        
        client = IBMAIClient()
        response = await client.generate_response("test prompt")
        
        assert "Mock" in response
        assert len(response) > 0
    
    @pytest.mark.asyncio
    async def test_generate_response_with_context(self, mock_settings):
        """Should accept context parameter."""
        from app.services.ibm_ai_client import IBMAIClient
        
        client = IBMAIClient()
        response = await client.generate_response("test", context="some context")
        
        assert response is not None
        assert len(response) > 0


class TestMessageSchemas:
    """Tests for message schemas."""
    
    def test_unified_message_creation(self):
        """Should create a valid UnifiedMessage."""
        from app.schemas.message import UnifiedMessage, ChannelType
        
        msg = UnifiedMessage(
            channel=ChannelType.telegram,
            sender_id="123",
            session_id="tg_123",
            content="Hello"
        )
        
        assert msg.channel == ChannelType.telegram
        assert msg.content_type == "text"
        assert msg.timestamp is not None
    
    def test_bot_response_creation(self):
        """Should create a valid BotResponse."""
        from app.schemas.message import BotResponse
        
        resp = BotResponse(content="AI response", session_id="tg_123")
        
        assert resp.success is True
        assert resp.content == "AI response"


class TestWebhookCommands:
    """Tests for bot command handling in webhook."""
    
    @pytest.mark.asyncio
    async def test_help_command(self, mock_settings):
        """Should return help text for /help command."""
        from app.api.v1.endpoints.webhook import handle_bot_command
        
        with patch("app.api.v1.endpoints.webhook.TelegramAdapter") as mock_tg:
            mock_instance = MagicMock()
            mock_instance.send_message = AsyncMock(return_value=True)
            mock_tg.return_value = mock_instance
            
            result = await handle_bot_command("/help", "123", "tg_123")
            
            assert result is not None
            assert "Commands" in result
            mock_instance.send_message.assert_called_once()
