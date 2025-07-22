from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

async def date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        # ЛИЧНЫЙ ЧАТ — Web App (iframe)
        keyboard = [
            [InlineKeyboardButton("Открыть календарь",
                                  web_app=WebAppInfo(url="https://earthwormxd.github.io/game-calendar-iframe/"))]
        ]
        await update.message.reply_text("Вот твой календарь 👇", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        # ГРУППА — обычная ссылка
        keyboard = [
            [InlineKeyboardButton("Открыть календарь (в браузере)",
                                  url="https://earthwormxd.github.io/game-calendar-iframe/")]
        ]
        await update.message.reply_text("Открой календарь по ссылке 👇", reply_markup=InlineKeyboardMarkup(keyboard))

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎲 Функция кубов пока в разработке!")

async def set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("date", "Календарь сессий"),
        BotCommand("dice", "Кубы")
    ])

def main():
    app = ApplicationBuilder().token(TOKEN).post_init(set_commands).build()

    app.add_handler(CommandHandler("date", date))
    app.add_handler(CommandHandler("dice", dice))

    app.run_polling()

if __name__ == '__main__':
    main()
