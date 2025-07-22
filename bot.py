from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import random

TOKEN = os.getenv("BOT_TOKEN")

# === /date ===
async def date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        keyboard = [
            [InlineKeyboardButton("Открыть календарь",
                                  web_app=WebAppInfo(url="https://earthwormxd.github.io/game-calendar-iframe/"))]
        ]
        await update.message.reply_text("Вот твой календарь 👇", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        keyboard = [
            [InlineKeyboardButton("Открыть календарь (в браузере)",
                                  url="https://earthwormxd.github.io/game-calendar-iframe/")]
        ]
        await update.message.reply_text("Открой календарь по ссылке 👇", reply_markup=InlineKeyboardMarkup(keyboard))

# === /dice ===
async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("🎲 d4", callback_data="roll_d4"),
         InlineKeyboardButton("🎲 d6", callback_data="roll_d6")],
        [InlineKeyboardButton("🎲 d8", callback_data="roll_d8"),
         InlineKeyboardButton("🎲 d10", callback_data="roll_d10")],
        [InlineKeyboardButton("🎲 d12", callback_data="roll_d12"),
         InlineKeyboardButton("🎲 d20", callback_data="roll_d20")],
    ]
    await update.message.reply_text("Выбери куб для броска:", reply_markup=InlineKeyboardMarkup(buttons))

# === Обработка бросков ===
async def handle_roll_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("roll_d"):
        dice_type = int(data.split("_")[1][1:])  # d6 → 6

        if dice_type == 6:
            # Используем встроенную анимацию Telegram
            await query.message.reply_dice(emoji="🎲")
        else:
            result = random.randint(1, dice_type)
            await query.message.reply_text(f"🎲 Бросок d{dice_type}: *{result}*", parse_mode="Markdown")

# === Установка команд ===
async def set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("date", "Календарь сессий"),
        BotCommand("dice", "Кубы")
    ])

# === Запуск ===
def main():
    app = ApplicationBuilder().token(TOKEN).post_init(set_commands).build()

    app.add_handler(CommandHandler("date", date))
    app.add_handler(CommandHandler("dice", dice))
    app.add_handler(CallbackQueryHandler(handle_roll_callback))

    app.run_polling()

if __name__ == '__main__':
    main()
