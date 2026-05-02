import asyncio
from app.services.channel_adapters.telegram import TelegramAdapter

async def main():
    adapter = TelegramAdapter()
    await adapter.send_message(chat_id="8214043955", text="Test message from python script")

asyncio.run(main())
