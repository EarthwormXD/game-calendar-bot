from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    WebAppInfo,
    BotCommand,
    BotCommandScopeDefault,
    BotCommandScopeAllGroupChats,
)
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import os
import asyncio
from aiohttp import web
import random

TOKEN = os.getenv("BOT_TOKEN")

# ====== /dice — Бросок кубиков ======
async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dice_buttons = [
        [InlineKeyboardButton("🎲 d4", callback_data="roll_d4"),
         InlineKeyboardButton("🎲 d6", callback_data="roll_d6")],
        [InlineKeyboardButton("🎲 d8", callback_data="roll_d8"),
         InlineKeyboardButton("🎲 d10", callback_data="roll_d10")],
        [InlineKeyboardButton("🎲 d12", callback_data="roll_d12"),
         InlineKeyboardButton("🎲 d20", callback_data="roll_d20")]
    ]
    await update.message.reply_text("Выбери кубик для броска:", reply_markup=InlineKeyboardMarkup(dice_buttons))

# ====== /date — Календарь ======
async def date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        keyboard = [[
            InlineKeyboardButton("Открыть календарь", web_app=WebAppInfo(url="https://earthwormxd.github.io/game-calendar-iframe/"))
        ]]
    else:
        keyboard = [[
            InlineKeyboardButton("Открыть календарь (в браузере)", url="https://earthwormxd.github.io/game-calendar-iframe/")
        ]]
    await update.message.reply_text("Вот календарь 👇", reply_markup=InlineKeyboardMarkup(keyboard))

# ====== Обработка нажатий на кубы ======
async def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    dice_type = query.data.split("_")[1]  # например "d20"
    sides = int(dice_type)
    result = random.randint(1, sides)
    await query.edit_message_text(f"🎲 Брошен {dice_type} → результат: {result}")

# ====== Установка команд ======
async def set_commands(app):
    commands = [
        BotCommand("dice", "Бросить кубики"),
        BotCommand("date", "Календарь сессий")
    ]
    await app.bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    await app.bot.set_my_commands(commands, scope=BotCommandScopeAllGroupChats())

# ====== Запуск Telegram бота ======
async def start_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    await set_commands(app)

    app.add_handler(CommandHandler("dice", dice))
    app.add_handler(CommandHandler("date", date))
    app.add_handler(CallbackQueryHandler(roll_dice, pattern="^roll_"))

    await app.initialize()
    await app.start()
    print("🤖 Telegram Bot запущен")

# ====== Пустой HTTP-сервер для Render ======
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

# ====== Основной запуск ======
async def main():
    await asyncio.gather(
        start_bot(),
        start_web_server()
    )

if __name__ == "__main__":
    asyncio.run(main())
