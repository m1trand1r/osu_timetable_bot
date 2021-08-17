import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# from config import TOKEN

# Config string for docker image
TG_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

bot = Bot(token=TG_API_TOKEN)
dp = Dispatcher(bot)




@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    student = types.InlineKeyboardButton('Студент')
    teacher = types.InlineKeyboardButton('Преподаватель')


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text + f' {msg.from_user.id}')


if __name__ == '__main__' :
    executor.start_polling(dp)