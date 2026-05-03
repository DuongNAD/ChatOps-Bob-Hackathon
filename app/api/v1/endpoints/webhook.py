"""
Webhook endpoints for receiving messages from chat platforms.

This module provides webhook endpoints for various chat platforms
to send incoming messages to the ChatOps gateway.
"""

import logging
from fastapi import APIRouter, Request, BackgroundTasks

from app.services.channel_adapters.telegram import TelegramAdapter
from app.services.message_router import process_incoming_message
from app.models.conversation import SessionManager
from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Bot command handlers
HELP_TEXT = """🤖 **ChatOps-Bob Gateway — Commands**

📌 **Available Commands:**
• `/help` — Show this help message
• `/status` — Check system status
• `/history` — View your recent conversation history
• `/bob <task>` — Send a task to IBM Bob AI in VS Code

💡 **Examples:**
• `/bob Write a Python function to calculate Fibonacci series`
• `/bob Fix the bug in my sorting algorithm`

Or just type any message to chat with **IBM Granite AI**!

_Powered by IBM Watsonx AI — ibm/granite-3-8b-instruct_
"""

STATUS_TEXT = """📊 **System Status**

🏷️ **Service:** {service}
📦 **Version:** {version}
🤖 **AI Engine:** {ai_mode}
🧠 **Model:** `{model}`
📡 **Telegram:** Connected ✅
💾 **Database:** {db_status}

_Total messages: {total_msgs}_
"""


async def handle_bot_command(command: str, sender_id: str, session_id: str) -> str | None:
    """
    Handle built-in bot commands (/help, /status, /history).
    
    Returns response text if command was handled, None otherwise.
    """
    telegram = TelegramAdapter()
    
    if command == "/help" or command == "/start":
        await telegram.send_message(chat_id=sender_id, text=HELP_TEXT)
        return HELP_TEXT
    
    elif command == "/status":
        import aiosqlite
        from app.models.conversation import get_db_path
        
        db_status = "Healthy ✅"
        total_msgs = 0
        try:
            async with aiosqlite.connect(get_db_path()) as db:
                cursor = await db.execute("SELECT COUNT(*) FROM messages")
                total_msgs = (await cursor.fetchone())[0]
        except Exception:
            db_status = "Error ❌"
        
        status = STATUS_TEXT.format(
            service=settings.APP_NAME,
            version=settings.APP_VERSION,
            ai_mode="🧪 Mock Mode" if settings.USE_MOCK_AI else "🟢 Live",
            model=settings.WATSONX_MODEL,
            db_status=db_status,
            total_msgs=total_msgs
        )
        await telegram.send_message(chat_id=sender_id, text=status)
        return status
    
    elif command == "/history":
        session_mgr = SessionManager()
        history = await session_mgr.get_history(session_id=session_id, limit=5)
        
        if history:
            response = f"📜 **Your Recent History** (Session: `{session_id}`)\n\n{history}"
        else:
            response = "📜 No conversation history found for your session."
        
        await telegram.send_message(chat_id=sender_id, text=response)
        return response
    
    return None


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
        
        # Check for built-in commands first (handle synchronously for fast response)
        content_lower = message.content.strip().lower()
        if content_lower in ("/help", "/start", "/status", "/history"):
            background_tasks.add_task(
                handle_bot_command,
                content_lower,
                message.sender_id,
                message.session_id
            )
            return {"status": "ok", "command": content_lower}
        
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