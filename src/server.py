import os

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor

from config import TOKEN
from value_holders import ValueHolder, SelectorsHolder
from scraper import Scraper

# Config string for docker image
# TG_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

# init value holder
value_holder = ValueHolder()

# init scraper class
req = Scraper()

# init selector holders
selectors = SelectorsHolder()


# для json запроса
# req = "https://www.osu.ru/pages/schedule/?who=1&what=1&bot=1&filial=1&group=11852&mode=full"


def choose_filial():
    if selectors.filial is None and selectors.filial_reversed is None:
        selectors.filial, selectors.filial_reversed = req.get_filial()
    items = []
    for fil in selectors.filial:
        items.append(types.InlineKeyboardButton(fil, callback_data='filial_' + str(selectors.filial[fil])))
    return items


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    """
    Choose phase of bot entrypoint
    :param message: command of start
    :return:
    """
    markup = types.InlineKeyboardMarkup(row_width=1)
    filials = choose_filial()
    markup.add(*filials)
    value_holder.chat_id_holder = message.chat.id
    # await state_holder.next()
    await bot.send_message(message.chat.id,
                           "Добро пожаловать в бот с расписанием!\n"
                           "Выберите филиал:",
                           reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data.startswith('filial_'))
async def process_start_command(call):
    value_holder.filial = call.data.split('_')[1]
    value_holder.message_id_holder = call.message.message_id
    markup = types.InlineKeyboardMarkup()
    student = types.InlineKeyboardButton('Студент', callback_data='type_student')
    teacher = types.InlineKeyboardButton('Преподаватель', callback_data='type_teacher')
    cancel = types.InlineKeyboardButton('Назад', callback_data='cFilial')
    markup.add(*[student, teacher, cancel])
    await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
                                message_id=value_holder.message_id_holder,
                                text="Выберите студент вы или преподаватель",
                                reply_markup=markup
                                )


@dp.callback_query_handler(lambda call: call.data.startswith('cFilial'))
async def process_start_command(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    filials = choose_filial()
    markup.add(*filials)
    # await bot.delete_message(call.message.chat.id, call.message.message_id)
    # value_holder.message_id_holder = None
    await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
                                message_id=value_holder.message_id_holder,
                                text="Добро пожаловать в бот с расписанием!\n"
                                     "Выберите филиал:",
                                reply_markup=markup)


# @dp.callback_query_handler(lambda call: call.data.startswith('type_'))
# async def choose_faculty(call: types.CallbackQuery):
#     await bot.send_message(call.message.chat.id,
#                            f"Вы выбрали {'студент' if call.data == 'type_student' else 'преподаватель'}")


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text + f' {msg.from_user.id}')


if __name__ == '__main__':
    executor.start_polling(dp)
