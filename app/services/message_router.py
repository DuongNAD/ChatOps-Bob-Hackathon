"""
Message router for processing incoming messages through the ChatOps pipeline.

This module orchestrates the flow of messages from users through the AI engine
and back to the appropriate channel.
"""

import logging
import os
from app.schemas.message import UnifiedMessage
from app.models.conversation import SessionManager
from app.services.ibm_ai_client import IBMAIClient
from app.services.channel_adapters.telegram import TelegramAdapter
from app.services.rpa_controller import RPAController

# Configure logging
logger = logging.getLogger(__name__)


async def process_incoming_message(message: UnifiedMessage) -> str:
    """
    Process an incoming message through the ChatOps pipeline.
    
    This function orchestrates the complete message flow:
    1. Save user message to database
    2. Retrieve conversation history
    3. Generate AI response using IBM Watsonx AI
    4. Save AI response to database
    5. Send response back to user via their channel
    
    Args:
        message: The unified message object from any channel
        
    Returns:
        str: The AI-generated response text
        
    Note:
        If any error occurs, an error message is sent to the user
        and the error is logged.
    """
    session_manager = SessionManager()
    ai_client = IBMAIClient()
    telegram_adapter = TelegramAdapter()
    
    try:
        # Check for special RPA command
        if message.content.startswith("/bob "):
            # Extract command (remove "/bob " prefix)
            bob_command = message.content[5:].strip()
            
            rpa = RPAController()
            
            # Check if RPA is busy
            if rpa.is_busy:
                await telegram_adapter.send_message(
                    chat_id=message.sender_id,
                    text="⏳ System is processing another command. Please wait..."
                )
                return "busy"
            
            # Notify user that command is being processed
            await telegram_adapter.send_message(
                chat_id=message.sender_id,
                text=f"🤖 Sending command to IBM Bob:\n`{bob_command}`\n\nPlease wait 20-30 seconds..."
            )
            
            # Execute RPA
            result = await rpa.execute_bob_command(bob_command)
            
            if result["success"]:
                # Send screenshot if available
                if result.get("screenshot_path") and os.path.exists(result["screenshot_path"]):
                    await telegram_adapter.send_photo(
                        chat_id=message.sender_id,
                        photo_path=result["screenshot_path"],
                        caption="📸 Result from IBM Bob"
                    )
                
                # Send code text if available
                if result.get("code_text"):
                    await telegram_adapter.send_message(
                        chat_id=message.sender_id,
                        text=f"📝 Code:\n```\n{result['code_text'][:3000]}\n```"
                    )
                else:
                    await telegram_adapter.send_message(
                        chat_id=message.sender_id,
                        text="✅ Command sent to Bob. See screenshot above."
                    )
            else:
                await telegram_adapter.send_message(
                    chat_id=message.sender_id,
                    text=f"❌ RPA Error: {result.get('error', 'Unknown error')}"
                )
            
            return result.get("code_text", "RPA completed")
        
        # Step 1: Save user message to database
        logger.info(f"[ROUTER] Processing message from session {message.session_id}")
        logger.info(f"[ROUTER] Message content: {message.content}")
        logger.info(f"[ROUTER] Sender ID: {message.sender_id}")
        logger.info(f"[ROUTER] Channel: {message.channel}")
        await session_manager.save_message(
            session_id=message.session_id,
            role="user",
            content=message.content
        )
        logger.debug(f"Saved user message: {message.content[:50]}...")
        
        # Step 2: Retrieve conversation history
        history = await session_manager.get_history(
            session_id=message.session_id,
            limit=5
        )
        logger.debug(f"Retrieved conversation history ({len(history)} chars)")
        
        # Step 3: Generate AI response
        logger.info("Generating AI response...")
        ai_response = await ai_client.generate_response(
            prompt=message.content,
            context=history
        )
        logger.info(f"AI response generated ({len(ai_response)} chars)")
        
        if not ai_response or ai_response.strip() == "":
            ai_response = "⚠️ IBM Watsonx AI processed successfully but returned an empty result. Please provide more information for your question."
            logger.warning("AI returned empty response, using fallback text.")
        
        # Step 4: Save AI response to database
        await session_manager.save_message(
            session_id=message.session_id,
            role="assistant",
            content=ai_response
        )
        logger.debug("Saved AI response to database")
        
        # Step 5: Send response back to user via their channel
        # Currently only Telegram is supported
        if message.channel.value == "telegram":
            logger.info(f"Sending to Telegram. Type: {type(ai_response)}, Repr: {repr(ai_response)}")
            success = await telegram_adapter.send_message(
                chat_id=message.sender_id,
                text=ai_response
            )
            
            if success:
                logger.info(f"Response sent successfully to {message.sender_id}")
            else:
                logger.warning(f"Failed to send response to {message.sender_id}")
        else:
            logger.warning(f"Unsupported channel: {message.channel.value}")
        
        return ai_response
        
    except Exception as e:
        # Log the error
        logger.error(f"Error processing message: {e}", exc_info=True)
        
        # Prepare error message for user
        error_message = (
            "⚠️ **Sorry!**\n\n"
            "An error occurred while processing your message. "
            "Please try again later.\n\n"
            f"_Error code: {type(e).__name__}_"
        )
        
        # Try to send error message to user
        try:
            if message.channel.value == "telegram":
                await telegram_adapter.send_message(
                    chat_id=message.sender_id,
                    text=error_message
                )
                logger.info("Error message sent to user")
        except Exception as send_error:
            logger.error(f"Failed to send error message to user: {send_error}")
        
        # Re-raise the exception for upstream handling if needed
        raise


# Made with Bob