import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = "https://earthwormxd.github.io/telegram-calendar-app/"  # Замени на свой URL

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Открыть календарь 🗓", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    await update.message.reply_text(
        "Нажми на кнопку, чтобы открыть календарь:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
