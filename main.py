import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils import executor
import os

# Токен бота из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# URL на твою GitHub Pages с календарем
CALENDAR_URL = "https://earthwormxd.github.io/telegram-calendar-app/"

@dp.message_handler(commands=["start"])
async def send_calendar_button(message: types.Message):
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text="Открыть календарь 🗓",
            web_app=WebAppInfo(url=CALENDAR_URL)
        )
    )
    await message.answer("Нажми кнопку ниже, чтобы открыть календарь:", reply_markup=keyboard)

if __name__ == "__main__":
    executor.start_polling(dp)
