from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import random
from dotenv import load_dotenv

load_dotenv()

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
async def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("D4", callback_data="roll_d4"),
            InlineKeyboardButton("D6", callback_data="roll_d6"),
            InlineKeyboardButton("D8", callback_data="roll_d8"),
        ],
        [
            InlineKeyboardButton("D10", callback_data="roll_d10"),
            InlineKeyboardButton("D12", callback_data="roll_d12"),
            InlineKeyboardButton("D20", callback_data="roll_d20"),
        ],
        [
            InlineKeyboardButton("D100", callback_data="roll_d100"),
        ],
    ]
    await update.message.reply_text("Выбери кубик 🎲", reply_markup=InlineKeyboardMarkup(keyboard))

# === Обработка нажатий на кубики ===
async def handle_roll_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("roll_d"):
        dice_type = int(data.split("_")[1][1:])  # Пример: "roll_d20" → 20
        result = random.randint(1, dice_type)
        user = query.from_user
        print(f"[LOG] {user.username or user.first_name} бросил d{dice_type} → результат: {result}")
        await query.message.reply_text(f"🎲 d{dice_type} → *{result}*", parse_mode="Markdown")

# === Команды ===
async def set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("date", "Календарь сессий"),
        BotCommand("dice", "Кубы")
    ])

# === Основной запуск ===
def main():
    app = ApplicationBuilder().token(TOKEN).post_init(set_commands).build()

    app.add_handler(CommandHandler("date", date))
    app.add_handler(CommandHandler("dice", roll_dice))
    app.add_handler(CallbackQueryHandler(handle_roll_callback))

    app.run_polling()

if __name__ == '__main__':
    main()
