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
    query = update.callback_query
    await query.answer()
    dice_type = query.data.split("_")[1]  # например "d20"
    sides = int(dice_type)
    result = random.randint(1, sides)

    user = query.from_user
    chat_id = query.message.chat.id

    print(f"[LOG] {user.username or user.first_name} бросил {dice_type} → результат: {result}")

    # Вместо изменения кнопок — просто отправим новое сообщение
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"🎲 Брошен {dice_type} → результат: {result}"
    )

# === Обработка нажатий ===
async def handle_roll_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Закрыть "часики"

    data = query.data
    if data.startswith("roll_d"):
        dice_type = int(data.split("_")[1][1:])  # Пример: "roll_d20" → 20
        result = random.randint(1, dice_type)
        await query.edit_message_text(f"🎲 Бросок {dice_type}-гранного куба: *{result}*", parse_mode="Markdown")

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
