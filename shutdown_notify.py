import asyncio
import os
import socket
from dotenv import load_dotenv
from telegram import Bot

load_dotenv("/home/master/Panel/.env")

TOKEN = os.getenv("TOKEN")
OWNER_ID = os.getenv("OWNER_ID")

async def main():
    bot = Bot(TOKEN)

    await bot.send_message(
        chat_id=OWNER_ID,
        text=f"🔴 {socket.gethostname()} is shutting down"
    )

    await bot.shutdown()

asyncio.run(main())