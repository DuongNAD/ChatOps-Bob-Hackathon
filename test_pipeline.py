import asyncio
from app.schemas.message import UnifiedMessage, ChannelType
from app.services.message_router import process_incoming_message

async def main():
    message = UnifiedMessage(
        channel=ChannelType.telegram,
        sender_id="8214043955",
        session_id="tg_8214043955",
        content="hello",
        content_type="text"
    )
    result = await process_incoming_message(message)
    print("FINAL RESULT:", repr(result))

asyncio.run(main())
