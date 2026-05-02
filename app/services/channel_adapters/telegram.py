"""
Telegram Bot adapter for ChatOps gateway.

This module provides an adapter for communicating with Telegram Bot API,
including parsing incoming webhooks and sending messages.
"""

import logging
from typing import Optional
import httpx

from app.schemas.message import UnifiedMessage, ChannelType
from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Telegram message length limit
TELEGRAM_MAX_LENGTH = 4096


class TelegramAdapter:
    """
    Adapter for Telegram Bot API integration.
    
    Handles parsing incoming webhook payloads and sending messages
    through the Telegram Bot API.
    """
    
    def __init__(self):
        """Initialize the Telegram adapter with bot token from settings."""
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.api_base_url = f"https://api.telegram.org/bot{self.bot_token}"
        logger.info("Telegram adapter initialized")
    
    def parse_webhook(self, payload: dict) -> UnifiedMessage:
        """
        Parse incoming Telegram webhook payload into UnifiedMessage format.
        
        Args:
            payload: The webhook payload from Telegram
            
        Returns:
            UnifiedMessage: Standardized message object
            
        Raises:
            KeyError: If required fields are missing from payload
        """
        try:
            # Extract message data safely
            message = payload.get("message", {})
            chat = message.get("chat", {})
            
            # Get chat_id (required)
            chat_id = chat.get("id")
            if chat_id is None:
                raise KeyError("Missing 'chat.id' in webhook payload")
            
            # Get message text (default to empty string if not present)
            content = message.get("text", "")
            
            # Create session_id in format "tg_{chat_id}"
            session_id = f"tg_{chat_id}"
            
            # Convert chat_id to string for sender_id
            sender_id = str(chat_id)
            
            logger.debug(f"Parsed Telegram message from chat {chat_id}")
            
            return UnifiedMessage(
                channel=ChannelType.telegram,
                sender_id=sender_id,
                session_id=session_id,
                content=content,
                content_type="text"
            )
            
        except KeyError as e:
            logger.error(f"Failed to parse Telegram webhook: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error parsing Telegram webhook: {e}")
            raise
    
    async def send_message(self, chat_id: str, text: str) -> bool:
        """
        Send a message to a Telegram chat.
        
        Handles long messages by splitting them into chunks if they exceed
        Telegram's 4096 character limit.
        
        Args:
            chat_id: The Telegram chat ID to send the message to
            text: The message text to send (supports Markdown)
            
        Returns:
            bool: True if all messages sent successfully, False otherwise
        """
        try:
            # Split message if it exceeds Telegram's limit
            if len(text) > TELEGRAM_MAX_LENGTH:
                return await self._send_long_message(chat_id, text)
            
            # Send single message
            return await self._send_single_message(chat_id, text)
            
        except Exception as e:
            logger.error(f"Failed to send message to chat {chat_id}: {e}")
    
    async def send_photo(self, chat_id: str, photo_path: str, caption: str = "") -> bool:
        """
        Send a photo to a Telegram chat.
        
        Args:
            chat_id: The Telegram chat ID to send the photo to
            photo_path: Path to the photo file to send
            caption: Optional caption for the photo (supports Markdown)
            
        Returns:
            bool: True if photo sent successfully, False otherwise
        """
        url = f"{self.api_base_url}/sendPhoto"
        
        try:
            # Prepare the multipart form data
            data = {
                "chat_id": chat_id,
            }
            
            # Add caption if provided
            if caption:
                data["caption"] = caption
                data["parse_mode"] = "Markdown"
            
            # Open and send the photo file
            async with httpx.AsyncClient() as client:
                with open(photo_path, "rb") as photo_file:
                    files = {
                        "photo": photo_file
                    }
                    
                    response = await client.post(
                        url, 
                        data=data, 
                        files=files, 
                        timeout=30.0
                    )
                    
                    if response.status_code == 200:
                        logger.info(f"Photo sent successfully to chat {chat_id}")
                        return True
                    else:
                        logger.error(
                            f"Failed to send photo to chat {chat_id}: "
                            f"Status {response.status_code}, Response: {response.text}"
                        )
                        return False
                        
        except FileNotFoundError:
            logger.error(f"Photo file not found: {photo_path}")
            return False
        except httpx.TimeoutException:
            logger.error(f"Timeout sending photo to chat {chat_id}")
            return False
        except Exception as e:
            logger.error(f"Error sending photo to chat {chat_id}: {e}")
            return False
            return False
    
    async def _send_single_message(self, chat_id: str, text: str) -> bool:
        """
        Send a single message via Telegram Bot API.
        
        Args:
            chat_id: The Telegram chat ID
            text: The message text (must be <= 4096 characters)
            
        Returns:
            bool: True if successful, False otherwise
        """
        url = f"{self.api_base_url}/sendMessage"
        
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=10.0)
                
                if response.status_code == 200:
                    logger.info(f"Message sent successfully to chat {chat_id}")
                    return True
                else:
                    logger.error(
                        f"Failed to send message to chat {chat_id}: "
                        f"Status {response.status_code}, Response: {response.text}"
                    )
                    return False
                    
        except httpx.TimeoutException:
            logger.error(f"Timeout sending message to chat {chat_id}")
            return False
        except Exception as e:
            logger.error(f"Error sending message to chat {chat_id}: {e}")
            return False
    
    async def _send_long_message(self, chat_id: str, text: str) -> bool:
        """
        Send a long message by splitting it into multiple chunks.
        
        Args:
            chat_id: The Telegram chat ID
            text: The long message text (> 4096 characters)
            
        Returns:
            bool: True if all chunks sent successfully, False otherwise
        """
        logger.info(
            f"Message length {len(text)} exceeds limit, splitting into chunks"
        )
        
        # Split text into chunks of TELEGRAM_MAX_LENGTH
        chunks = []
        for i in range(0, len(text), TELEGRAM_MAX_LENGTH):
            chunk = text[i:i + TELEGRAM_MAX_LENGTH]
            chunks.append(chunk)
        
        logger.debug(f"Split message into {len(chunks)} chunks")
        
        # Send each chunk
        all_success = True
        for idx, chunk in enumerate(chunks, 1):
            success = await self._send_single_message(chat_id, chunk)
            if not success:
                logger.error(f"Failed to send chunk {idx}/{len(chunks)}")
                all_success = False
        
        return all_success


# Made with Bob