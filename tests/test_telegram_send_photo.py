"""
Tests for Telegram send_photo functionality.

This module tests the send_photo method in TelegramAdapter.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock, mock_open
from app.services.channel_adapters.telegram import TelegramAdapter


class TestTelegramSendPhoto:
    """Test send_photo method."""
    
    @pytest.mark.asyncio
    async def test_send_photo_success(self):
        """Test successful photo sending."""
        adapter = TelegramAdapter()
        
        # Mock httpx.AsyncClient
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        # Mock file opening
        mock_file_data = b"fake image data"
        
        with patch('httpx.AsyncClient', return_value=mock_client), \
             patch('builtins.open', mock_open(read_data=mock_file_data)):
            
            result = await adapter.send_photo(
                chat_id="123456",
                photo_path="/path/to/photo.png",
                caption="Test caption"
            )
            
            # Verify result
            assert result is True
            
            # Verify httpx.post was called
            mock_client.post.assert_called_once()
            call_args = mock_client.post.call_args
            
            # Verify URL
            assert "sendPhoto" in call_args[0][0]
            
            # Verify data contains chat_id and caption
            assert call_args[1]["data"]["chat_id"] == "123456"
            assert call_args[1]["data"]["caption"] == "Test caption"
            assert call_args[1]["data"]["parse_mode"] == "Markdown"
    
    @pytest.mark.asyncio
    async def test_send_photo_without_caption(self):
        """Test photo sending without caption."""
        adapter = TelegramAdapter()
        
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        mock_file_data = b"fake image data"
        
        with patch('httpx.AsyncClient', return_value=mock_client), \
             patch('builtins.open', mock_open(read_data=mock_file_data)):
            
            result = await adapter.send_photo(
                chat_id="123456",
                photo_path="/path/to/photo.png"
            )
            
            # Verify result
            assert result is True
            
            # Verify data does NOT contain caption or parse_mode
            call_args = mock_client.post.call_args
            assert "caption" not in call_args[1]["data"]
            assert "parse_mode" not in call_args[1]["data"]
    
    @pytest.mark.asyncio
    async def test_send_photo_with_empty_caption(self):
        """Test photo sending with empty caption."""
        adapter = TelegramAdapter()
        
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        mock_file_data = b"fake image data"
        
        with patch('httpx.AsyncClient', return_value=mock_client), \
             patch('builtins.open', mock_open(read_data=mock_file_data)):
            
            result = await adapter.send_photo(
                chat_id="123456",
                photo_path="/path/to/photo.png",
                caption=""
            )
            
            # Verify result
            assert result is True
            
            # Verify data does NOT contain caption or parse_mode (empty caption)
            call_args = mock_client.post.call_args
            assert "caption" not in call_args[1]["data"]
    
    @pytest.mark.asyncio
    async def test_send_photo_file_not_found(self):
        """Test photo sending when file doesn't exist."""
        adapter = TelegramAdapter()
        
        with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
            result = await adapter.send_photo(
                chat_id="123456",
                photo_path="/nonexistent/photo.png"
            )
            
            # Verify result is False
            assert result is False
    
    @pytest.mark.asyncio
    async def test_send_photo_api_error(self):
        """Test photo sending when API returns error."""
        adapter = TelegramAdapter()
        
        # Mock failed response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        mock_file_data = b"fake image data"
        
        with patch('httpx.AsyncClient', return_value=mock_client), \
             patch('builtins.open', mock_open(read_data=mock_file_data)):
            
            result = await adapter.send_photo(
                chat_id="123456",
                photo_path="/path/to/photo.png"
            )
            
            # Verify result is False
            assert result is False
    
    @pytest.mark.asyncio
    async def test_send_photo_timeout(self):
        """Test photo sending with timeout."""
        adapter = TelegramAdapter()
        
        mock_client = AsyncMock()
        mock_client.post.side_effect = Exception("Timeout")
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        mock_file_data = b"fake image data"
        
        with patch('httpx.AsyncClient', return_value=mock_client), \
             patch('builtins.open', mock_open(read_data=mock_file_data)):
            
            result = await adapter.send_photo(
                chat_id="123456",
                photo_path="/path/to/photo.png"
            )
            
            # Verify result is False
            assert result is False
    
    @pytest.mark.asyncio
    async def test_send_photo_with_long_caption(self):
        """Test photo sending with caption containing markdown."""
        adapter = TelegramAdapter()
        
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        mock_file_data = b"fake image data"
        
        long_caption = "**Bold text**\n`code block`\n_italic_"
        
        with patch('httpx.AsyncClient', return_value=mock_client), \
             patch('builtins.open', mock_open(read_data=mock_file_data)):
            
            result = await adapter.send_photo(
                chat_id="123456",
                photo_path="/path/to/photo.png",
                caption=long_caption
            )
            
            # Verify result
            assert result is True
            
            # Verify caption was sent correctly
            call_args = mock_client.post.call_args
            assert call_args[1]["data"]["caption"] == long_caption
            assert call_args[1]["data"]["parse_mode"] == "Markdown"


# Made with Bob