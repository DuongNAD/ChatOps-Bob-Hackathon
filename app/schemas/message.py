"""
Message schemas for unified communication across different channels.

This module defines the data models for handling messages from various
chat platforms (Telegram, Slack, Discord, Web) in a unified format.
"""

from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field


class ChannelType(str, Enum):
    """Supported communication channel types."""
    
    telegram = "telegram"
    slack = "slack"
    discord = "discord"
    web = "web"


class UnifiedMessage(BaseModel):
    """
    Unified message format for all incoming messages from different channels.
    
    This model standardizes messages from various platforms into a common format
    for processing by the ChatOps gateway.
    """
    
    channel: ChannelType = Field(
        ...,
        description="The channel/platform where the message originated"
    )
    sender_id: str = Field(
        ...,
        description="Unique identifier of the message sender"
    )
    session_id: str = Field(
        ...,
        description="Session identifier for conversation tracking"
    )
    content: str = Field(
        ...,
        description="The actual message content/text"
    )
    content_type: str = Field(
        default="text",
        description="Type of content (text, image, file, etc.)"
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when the message was received"
    )
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "channel": "telegram",
                "sender_id": "123456789",
                "session_id": "session_abc123",
                "content": "Hello, how can I help you?",
                "content_type": "text",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }


class BotResponse(BaseModel):
    """
    Response model for bot replies to user messages.
    
    This model represents the bot's response that will be sent back
    to the user through their respective channel.
    """
    
    content: str = Field(
        ...,
        description="The response message content to send to the user"
    )
    session_id: str = Field(
        ...,
        description="Session identifier to track the conversation"
    )
    success: bool = Field(
        default=True,
        description="Indicates whether the operation was successful"
    )
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "content": "I've processed your request successfully!",
                "session_id": "session_abc123",
                "success": True
            }
        }


# Made with Bob