import os
import asyncio
import random
import logging
from aiohttp import web
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    WebAppInfo,
    BotCommand,
    BotCommandScopeDefault,
    BotCommandScopeAllGroupChats,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ===== Настройка логирования =====
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===== Токен =====
TOKEN = os.getenv("BOT_TOKEN")

# ===== Команда /dice =====
async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Вызвана команда /dice")
    dice_buttons = [
        [InlineKeyboardButton("🎲 d4", callback_data="roll_d4"),
         InlineKeyboardButton("🎲 d6", callback_data="roll_d6")],
        [InlineKeyboardButton("🎲 d8", callback_data="roll_d8"),
         InlineKeyboardButton("🎲 d10", callback_data="roll_d10")],
        [InlineKeyboardButton("🎲 d12", callback_data="roll_d12"),
         InlineKeyboardButton("🎲 d20", callback_data="roll_d20")]
    ]
    await update.message.reply_text(
        "Выбери кубик для броска:", reply_markup=InlineKeyboardMarkup(dice_buttons)
    )

# ===== Команда /date =====
async def date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Вызвана команда /date")
    if update.effective_chat.type == "private":
        keyboard = [[
            InlineKeyboardButton(
                "Открыть календарь",
                web_app=WebAppInfo(url="https://earthwormxd.github.io/game-calendar-iframe/")
            )
        ]]
    else:
        keyboard = [[
            InlineKeyboardButton(
                "Открыть календарь (в браузере)",
                url="https://earthwormxd.github.io/game-calendar-iframe/"
            )
        ]]
    await update.message.reply_text(
        "Вот календарь 👇", reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ===== Обработка нажатий на кубы =====
async def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    logger.info(f"Нажата кнопка: {query.data}")

    try:
        dice_type = query.data.split("_")[1]  # Например: "d20"
        sides = int(dice_type)
        result = random.randint(1, sides)
        await query.edit_message_text(f"🎲 Брошен {dice_type} → результат: {result}")
    except Exception as e:
        logger.error(f"Ошибка при броске кубика: {e}")
        await query.edit_message_text("Произошла ошибка при броске кубика.")

# ===== Установка команд =====
async def set_commands(app):
    commands = [
        BotCommand("dice", "Бросить кубики"),
        BotCommand("date", "Календарь сессий")
    ]
    await app.bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    await app.bot.set_my_commands(commands, scope=BotCommandScopeAllGroupChats())
    logger.info("Команды установлены")

# ===== Запуск Telegram бота =====
async def start_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    await set_commands(app)

    app.add_handler(CommandHandler("dice", dice))
    app.add_handler(CommandHandler("date", date))
    app.add_handler(CallbackQueryHandler(roll_dice, pattern="^roll_"))

    await app.initialize()
    await app.start()
    logger.info("🤖 Telegram Bot запущен")

# ===== "Фейковый" веб-сервер =====
async def start_web_server():
    async def handle(request):
        logger.info("Ping от Render")
        return web.Response(text="Bot is running!")

    app = web.Application()
    app.router.add_get("/", handle)
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"🌐 HTTP сервер слушает порт {port}")

# ===== Основной запуск =====
async def main():
    await asyncio.gather(
        start_bot(),
        start_web_server()
    )

if __name__ == "__main__":
    asyncio.run(main())
