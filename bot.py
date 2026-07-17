
import os
import psutil
from dotenv import load_dotenv
from telegram import InputTextMessageContent,InlineQueryResultArticle, Update
from telegram.ext import InlineQueryHandler, ApplicationBuilder, CommandHandler, MessageHandler, filters, ChatMemberHandler

load_dotenv("/home/master/Panel/.env")

TOKEN = os.getenv("TOKEN")


bot_app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text("🟢 Серверный бот запущен")


async def status(update: Update, context):
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    await update.message.reply_text(
        f"🖥 Server Status\n\n"
        f"CPU: {cpu}%\n"
        f"RAM: {ram}%\n"
        f"DISK: {disk}%"
    )


bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("status", status))

async def start_bot():
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling()


async def stop_bot():
    await bot_app.updater.stop()
    await bot_app.stop()
    await bot_app.shutdown()
