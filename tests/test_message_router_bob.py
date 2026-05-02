"""
Tests for message router /bob command handling.

This module tests the RPA command routing in the message router.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.schemas.message import UnifiedMessage, ChannelType
from app.services.message_router import process_incoming_message


class TestMessageRouterBobCommand:
    """Test /bob command routing."""
    
    @pytest.mark.asyncio
    async def test_bob_command_triggers_rpa(self):
        """Test that /bob command triggers RPA controller."""
        # Create message with /bob command
        message = UnifiedMessage(
            channel=ChannelType.telegram,
            sender_id="123456",
            session_id="tg_123456",
            content="/bob Create a Python function",
            content_type="text"
        )
        
        # Mock RPAController
        mock_rpa_result = {
            "success": True,
            "screenshot_path": "/path/to/screenshot.png",
            "code_text": "def example(): pass",
            "error": ""
        }
        
        with patch('app.services.message_router.RPAController') as MockRPA, \
             patch('app.services.message_router.TelegramAdapter') as MockTelegram, \
             patch('os.path.exists', return_value=True):
            
            # Setup mocks
            mock_rpa_instance = MockRPA.return_value
            mock_rpa_instance.is_busy = False
            mock_rpa_instance.execute_bob_command = AsyncMock(return_value=mock_rpa_result)
            
            mock_telegram_instance = MockTelegram.return_value
            mock_telegram_instance.send_message = AsyncMock(return_value=True)
            mock_telegram_instance.send_photo = AsyncMock(return_value=True)
            
            # Execute
            result = await process_incoming_message(message)
            
            # Verify RPA was called with correct command
            mock_rpa_instance.execute_bob_command.assert_called_once_with("Create a Python function")
            
            # Verify messages were sent
            assert mock_telegram_instance.send_message.call_count >= 2  # Processing + result
            mock_telegram_instance.send_photo.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_bob_command_when_busy(self):
        """Test /bob command when RPA is busy."""
        message = UnifiedMessage(
            channel=ChannelType.telegram,
            sender_id="123456",
            session_id="tg_123456",
            content="/bob Another command",
            content_type="text"
        )
        
        with patch('app.services.message_router.RPAController') as MockRPA, \
             patch('app.services.message_router.TelegramAdapter') as MockTelegram:
            
            # Setup mocks - RPA is busy
            mock_rpa_instance = MockRPA.return_value
            mock_rpa_instance.is_busy = True
            
            mock_telegram_instance = MockTelegram.return_value
            mock_telegram_instance.send_message = AsyncMock(return_value=True)
            
            # Execute
            result = await process_incoming_message(message)
            
            # Verify result is "busy"
            assert result == "busy"
            
            # Verify busy message was sent
            mock_telegram_instance.send_message.assert_called_once()
            call_args = mock_telegram_instance.send_message.call_args
            assert "processing" in call_args[1]["text"].lower() or "busy" in call_args[1]["text"].lower()
    
    @pytest.mark.asyncio
    async def test_bob_command_sends_screenshot(self):
        """Test that /bob command sends screenshot when available."""
        message = UnifiedMessage(
            channel=ChannelType.telegram,
            sender_id="123456",
            session_id="tg_123456",
            content="/bob Test command",
            content_type="text"
        )
        
        mock_rpa_result = {
            "success": True,
            "screenshot_path": "/valid/path/screenshot.png",
            "code_text": "",
            "error": ""
        }
        
        with patch('app.services.message_router.RPAController') as MockRPA, \
             patch('app.services.message_router.TelegramAdapter') as MockTelegram, \
             patch('os.path.exists', return_value=True):
            
            mock_rpa_instance = MockRPA.return_value
            mock_rpa_instance.is_busy = False
            mock_rpa_instance.execute_bob_command = AsyncMock(return_value=mock_rpa_result)
            
            mock_telegram_instance = MockTelegram.return_value
            mock_telegram_instance.send_message = AsyncMock(return_value=True)
            mock_telegram_instance.send_photo = AsyncMock(return_value=True)
            
            await process_incoming_message(message)
            
            # Verify send_photo was called with correct parameters
            mock_telegram_instance.send_photo.assert_called_once_with(
                chat_id="123456",
                photo_path="/valid/path/screenshot.png",
                caption="📸 Result from IBM Bob"
            )
    
    @pytest.mark.asyncio
    async def test_bob_command_sends_code_text(self):
        """Test that /bob command sends code text when available."""
        message = UnifiedMessage(
            channel=ChannelType.telegram,
            sender_id="123456",
            session_id="tg_123456",
            content="/bob Generate code",
            content_type="text"
        )
        
        mock_rpa_result = {
            "success": True,
            "screenshot_path": "/path/screenshot.png",
            "code_text": "def hello():\n    print('Hello World')",
            "error": ""
        }
        
        with patch('app.services.message_router.RPAController') as MockRPA, \
             patch('app.services.message_router.TelegramAdapter') as MockTelegram, \
             patch('os.path.exists', return_value=True):
            
            mock_rpa_instance = MockRPA.return_value
            mock_rpa_instance.is_busy = False
            mock_rpa_instance.execute_bob_command = AsyncMock(return_value=mock_rpa_result)
            
            mock_telegram_instance = MockTelegram.return_value
            mock_telegram_instance.send_message = AsyncMock(return_value=True)
            mock_telegram_instance.send_photo = AsyncMock(return_value=True)
            
            await process_incoming_message(message)
            
            # Verify code text was sent
            calls = mock_telegram_instance.send_message.call_args_list
            code_sent = any("Code:" in str(call) or "```" in str(call) for call in calls)
            assert code_sent
    
    @pytest.mark.asyncio
    async def test_bob_command_handles_rpa_failure(self):
        """Test /bob command when RPA fails."""
        message = UnifiedMessage(
            channel=ChannelType.telegram,
            sender_id="123456",
            session_id="tg_123456",
            content="/bob Failing command",
            content_type="text"
        )
        
        mock_rpa_result = {
            "success": False,
            "screenshot_path": "",
            "code_text": "",
            "error": "RPA automation failed"
        }
        
        with patch('app.services.message_router.RPAController') as MockRPA, \
             patch('app.services.message_router.TelegramAdapter') as MockTelegram:
            
            mock_rpa_instance = MockRPA.return_value
            mock_rpa_instance.is_busy = False
            mock_rpa_instance.execute_bob_command = AsyncMock(return_value=mock_rpa_result)
            
            mock_telegram_instance = MockTelegram.return_value
            mock_telegram_instance.send_message = AsyncMock(return_value=True)
            
            await process_incoming_message(message)
            
            # Verify error message was sent
            calls = mock_telegram_instance.send_message.call_args_list
            error_sent = any("error" in str(call).lower() for call in calls)
            assert error_sent


class TestMessageRouterNormalMessages:
    """Test normal message routing (non-/bob commands)."""
    
    @pytest.mark.asyncio
    async def test_normal_message_uses_ai_pipeline(self):
        """Test that normal messages go through AI pipeline."""
        message = UnifiedMessage(
            channel=ChannelType.telegram,
            sender_id="123456",
            session_id="tg_123456",
            content="Hello, how are you?",
            content_type="text"
        )
        
        with patch('app.services.message_router.SessionManager') as MockSession, \
             patch('app.services.message_router.IBMAIClient') as MockAI, \
             patch('app.services.message_router.TelegramAdapter') as MockTelegram:
            
            # Setup mocks
            mock_session_instance = MockSession.return_value
            mock_session_instance.save_message = AsyncMock()
            mock_session_instance.get_history = AsyncMock(return_value="Previous conversation")
            
            mock_ai_instance = MockAI.return_value
            mock_ai_instance.generate_response = AsyncMock(return_value="AI response")
            
            mock_telegram_instance = MockTelegram.return_value
            mock_telegram_instance.send_message = AsyncMock(return_value=True)
            
            # Execute
            result = await process_incoming_message(message)
            
            # Verify AI pipeline was used
            mock_session_instance.save_message.assert_called()
            mock_ai_instance.generate_response.assert_called_once()
            mock_telegram_instance.send_message.assert_called_once()
            
            # Verify result is AI response
            assert result == "AI response"
    
    @pytest.mark.asyncio
    async def test_message_without_bob_prefix_not_rpa(self):
        """Test that messages without /bob prefix don't trigger RPA."""
        message = UnifiedMessage(
            channel=ChannelType.telegram,
            sender_id="123456",
            session_id="tg_123456",
            content="bob please help",  # No /bob prefix
            content_type="text"
        )
        
        with patch('app.services.message_router.RPAController') as MockRPA, \
             patch('app.services.message_router.SessionManager') as MockSession, \
             patch('app.services.message_router.IBMAIClient') as MockAI, \
             patch('app.services.message_router.TelegramAdapter') as MockTelegram:
            
            # Setup mocks
            mock_session_instance = MockSession.return_value
            mock_session_instance.save_message = AsyncMock()
            mock_session_instance.get_history = AsyncMock(return_value="")
            
            mock_ai_instance = MockAI.return_value
            mock_ai_instance.generate_response = AsyncMock(return_value="AI response")
            
            mock_telegram_instance = MockTelegram.return_value
            mock_telegram_instance.send_message = AsyncMock(return_value=True)
            
            # Execute
            await process_incoming_message(message)
            
            # Verify RPA was NOT instantiated
            MockRPA.assert_not_called()
            
            # Verify AI was used instead
            mock_ai_instance.generate_response.assert_called_once()


# Made with Bob