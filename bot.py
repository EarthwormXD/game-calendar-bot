from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        # ЛИЧНЫЙ ЧАТ — отправляем Web App (mini app с iframe)
        keyboard = [
            [InlineKeyboardButton("Открыть календарь",
                                  web_app=WebAppInfo(url="https://earthwormxd.github.io/game-calendar-iframe/"))]
        ]
        await update.message.reply_text("Вот твой календарь 👇", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        # ГРУППА — отправляем обычную ссылку
        keyboard = [
            [InlineKeyboardButton("Открыть календарь (в браузере)",
                                  url="https://earthwormxd.github.io/game-calendar-iframe/")]
        ]
        await update.message.reply_text("Открой календарь по ссылке 👇", reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == '__main__':
    main()
