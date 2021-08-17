import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN

# Config string for docker image
# TG_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    student = types.InlineKeyboardButton('Студент', callback_data='type_student')
    teacher = types.InlineKeyboardButton('Преподаватель', callback_data='type_teacher')
    markup.add(*[student, teacher])
    await bot.send_message(message.chat.id, "Добро пожаловать в бот с расписанием!\n"
                                            "Выберите студент вы или преподаватель",
                           reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data.startswith('type_'))
async def choose_faculty(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id, f"Вы выбрали {'студент' if call.data == 'type_student' else 'преподаватель'}" )


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text + f' {msg.from_user.id}')


if __name__ == '__main__' :
    executor.start_polling(dp)