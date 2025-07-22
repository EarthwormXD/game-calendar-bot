from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import asyncio
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")

# ====== Telegram Bot ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        keyboard = [[
            InlineKeyboardButton("Открыть календарь", web_app=WebAppInfo(url="https://earthwormxd.github.io/game-calendar-iframe/"))
        ]]
    else:
        keyboard = [[
            InlineKeyboardButton("Открыть календарь (в браузере)", url="https://earthwormxd.github.io/game-calendar-iframe/")
        ]]
    await update.message.reply_text("Вот твой календарь 👇", reply_markup=InlineKeyboardMarkup(keyboard))

async def start_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    await app.initialize()
    await app.start()
    print("🤖 Telegram Bot запущен")

# ====== "Фейковый" HTTP-сервер для Render ======
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 HTTP сервер слушает порт {port}")

# ====== Запуск ======
async def main():
    await asyncio.gather(
        start_bot(),
        start_web_server()
    )

if __name__ == "__main__":
    asyncio.run(main())
