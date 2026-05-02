"""
Webhook endpoints for receiving messages from chat platforms.

This module provides webhook endpoints for various chat platforms
to send incoming messages to the ChatOps gateway.
"""

import logging
from fastapi import APIRouter, Request, BackgroundTasks

from app.services.channel_adapters.telegram import TelegramAdapter
from app.services.message_router import process_incoming_message

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


@router.get("/webhook/telegram")
async def telegram_webhook_health():
    """
    Health check endpoint for Telegram webhook.
    
    Returns:
        dict: Status message indicating webhook is active
    """
    return {"status": "webhook active"}


@router.post("/webhook/telegram")
async def telegram_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Receive incoming messages from Telegram Bot API webhook.
    
    This endpoint receives webhook callbacks from Telegram, parses the message,
    and processes it asynchronously in the background to ensure quick response
    to Telegram (preventing webhook retries).
    
    Args:
        request: The FastAPI request object containing the webhook payload
        background_tasks: FastAPI background tasks for async processing
        
    Returns:
        dict: Status response to acknowledge receipt
        
    Note:
        Returns 200 OK immediately to prevent Telegram from retrying the webhook.
        Actual message processing happens in the background.
    """
    try:
        # Get raw JSON payload
        payload = await request.json()
        logger.info("Received Telegram webhook")
        logger.debug(f"Webhook payload: {payload}")
        
        # Parse webhook using TelegramAdapter
        telegram_adapter = TelegramAdapter()
        message = telegram_adapter.parse_webhook(payload)
        
        # Check if message content is empty or None
        if not message.content or message.content.strip() == "":
            logger.info("Ignoring empty message")
            return {"status": "ignored"}
        
        logger.info(
            f"Parsed message from {message.sender_id}: {message.content[:50]}..."
        )
        
        # Add message processing to background tasks
        # This allows us to return 200 OK immediately to Telegram
        background_tasks.add_task(process_incoming_message, message)
        
        logger.info("Message queued for background processing")
        return {"status": "ok"}
        
    except KeyError as e:
        # Missing required fields in webhook payload
        logger.error(f"Invalid webhook payload: {e}")
        return {"status": "error", "message": "Invalid payload"}
        
    except Exception as e:
        # Unexpected error
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        return {"status": "error", "message": "Internal error"}


# Made with Bob