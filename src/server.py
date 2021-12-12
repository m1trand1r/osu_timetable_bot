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

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# init value holder
value_holder = ValueHolder()

# init scraper class
req = Scraper()

# init selector holders
selectors = SelectorsHolder()

clear_reply_id = None

# для json запроса
# req = "https://www.osu.ru/pages/schedule/?who=1&what=1&bot=1&filial=1&group=11852&mode=full"


def choose_filial():
    if selectors.filial is None and selectors.filial_reversed is None:
        selectors.filial, selectors.filial_reversed = req.get_filial()
    items = []
    for fil in selectors.filial:
        items.append(types.InlineKeyboardButton(fil, callback_data='filial_' + str(selectors.filial[fil])))
    return items


def choose_faculty():
    if selectors.faculty is None and selectors.faculty_reversed is None:
        selectors.faculty, selectors.faculty_reversed = req.get_faculty(value_holder.filial)
    items = [types.InlineKeyboardButton(facult, callback_data='facult_' + str(facult)) for facult in selectors.faculty]
    items.append(types.InlineKeyboardButton('Назад', callback_data='cFacult'))
    return items


def choose_course_chair():
    if selectors.course_chair is None and selectors.course_chair_reversed is None:
        selectors.course_chair, selectors.course_chair_reversed = req.get_courses_chairs(value_holder.who,
                                                                                         value_holder.filial,
                                                                                         value_holder.faculty)
    items = [types.InlineKeyboardButton(value, callback_data='CCcall_' + str(value)) for value in
             selectors.course_chair]
    items.append(types.InlineKeyboardButton('Назад', callback_data='cCChair'))
    return items


def choose_group_teacher():
    if selectors.groups_teachers is None and selectors.groups_teachers_reversed is None:
        selectors.groups_teachers, selectors.groups_teachers_reversed = req.get_groups_teachers(value_holder.who,
                                                                                                value_holder.filial,
                                                                                                value_holder.faculty,
                                                                                                value_holder.course if value_holder.who == 1 else value_holder.chair
                                                                                                )
    items = [types.InlineKeyboardButton(value, callback_data='Gcall_' + str(value)) for value in
             selectors.groups_teachers]
    items.append(types.InlineKeyboardButton('Назад', callback_data='cGcall'))
    return items


@dp.message_handler(commands=['start', 'refresh'])
async def process_start_command(message: types.Message):
    """
    Choose phase of bot entrypoint
    :param message: command of start
    :return:
    """
    global value_holder
    value_holder = ValueHolder()
    markup = types.InlineKeyboardMarkup(row_width=1)
    filials = choose_filial()
    markup.add(*filials)
    value_holder.chat_id_holder = message.chat.id
    # await state_holder.next()
    await bot.send_message(message.chat.id,
                           '',
                           reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.chat.id,
                           "Добро пожаловать в бот с расписанием!\n"
                           "Выберите филиал:",
                           reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data.startswith('filial_'))
async def process_who_command(call: types.CallbackQuery):
    value_holder.filial = int(call.data.split('_')[1])
    value_holder.message_id_holder = call.message.message_id
    markup = types.InlineKeyboardMarkup()
    student = types.InlineKeyboardButton('Студент', callback_data='who_student')
    teacher = types.InlineKeyboardButton('Преподаватель', callback_data='who_teacher')
    cancel = types.InlineKeyboardButton('Назад', callback_data='cFilial')
    markup.add(*[student, teacher, cancel])
    await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
                                message_id=value_holder.message_id_holder,
                                text=f'Выбранный филиал - {selectors.filial_reversed[str(value_holder.filial)]}\n'
                                     f'Выберите студент вы или преподаватель',
                                reply_markup=markup
                                )


@dp.callback_query_handler(lambda call: call.data.startswith('who_'))
async def process_faculty_command(call: types.CallbackQuery):
    value_holder.who = selectors.who_reversed[call.data.split('_')[1]]
    markup = types.InlineKeyboardMarkup(row_width=2)
    items = choose_faculty()
    markup.add(*items)
    await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
                                message_id=value_holder.message_id_holder,
                                text=f'Выбранный филиал - {selectors.filial_reversed[str(value_holder.filial)]}\n'
                                     f'Вы - {selectors.who[str(value_holder.who)]}\n'
                                     f'Выберите факультет:',
                                reply_markup=markup
                                )


@dp.callback_query_handler(lambda call: call.data.startswith('facult_'))
async def process_course_command(call: types.CallbackQuery):
    value_holder.faculty = selectors.faculty[call.data.split('_')[1]]
    markup = types.InlineKeyboardMarkup(row_width=1)
    items = choose_course_chair()
    markup.add(*items)
    if value_holder.who == 1:
        await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
                                    message_id=value_holder.message_id_holder,
                                    text=f'Выбранный филиал - {selectors.filial_reversed[str(value_holder.filial)]}\n'
                                         f'Вы - {selectors.who[str(value_holder.who)]}\n'
                                         f'Выбранный факультет - {selectors.faculty_reversed[str(value_holder.faculty)]}\n'
                                         f'Выберите курс:',
                                    reply_markup=markup
                                    )
    else:
        await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
                                    message_id=value_holder.message_id_holder,
                                    text=f'Выбранный филиал - {selectors.filial_reversed[str(value_holder.filial)]}\n'
                                         f'Вы - {selectors.who[str(value_holder.who)]}\n'
                                         f'Выбранный факультет - {selectors.faculty_reversed[str(value_holder.faculty)]}\n'
                                         f'Выберите кафедру:',
                                    reply_markup=markup
                                    )


@dp.callback_query_handler(lambda call: call.data.startswith('CCcall_'))
async def process_group_command(call):
    if value_holder.who == 1:
        value_holder.course = selectors.course_chair[call.data.split('_')[1]]
    else:
        value_holder.chair = selectors.course_chair[call.data.split('_')[1]]
    items = choose_group_teacher()
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(*items)
    if value_holder.who == 1:
        await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
                                    message_id=value_holder.message_id_holder,
                                    text=f'Выбранный филиал - {selectors.filial_reversed[str(value_holder.filial)]}\n'
                                         f'Вы - {selectors.who[str(value_holder.who)]}\n'
                                         f'Выбранный факультет - {selectors.faculty_reversed[str(value_holder.faculty)]}\n'
                                         f'Выбранный курс - {selectors.course_chair_reversed[str(value_holder.course)]}\n'
                                         f'Выберите группу:',
                                    reply_markup=markup
                                    )
    else:
        await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
                                    message_id=value_holder.message_id_holder,
                                    text=f'Выбранный филиал - {selectors.filial_reversed[str(value_holder.filial)]}\n'
                                         f'Вы - {selectors.who[str(value_holder.who)]}\n'
                                         f'Выбранный факультет - {selectors.faculty_reversed[str(value_holder.faculty)]}\n'
                                         f'Выбранная кафедра - {selectors.course_chair_reversed[str(value_holder.chair)]}\n'
                                         f'Выберите преподавателя:',
                                    reply_markup=markup
                                    )


@dp.callback_query_handler(lambda call: call.data.startswith('Gcall_'))
async def process_confirm(call):
    if value_holder.who == 1:
        value_holder.group = selectors.groups_teachers[call.data.split('_')[1]]
    else:
        value_holder.teacher = selectors.groups_teachers[call.data.split('_')[1]]
    markup = types.InlineKeyboardMarkup()
    save = types.InlineKeyboardButton('Сохранить', callback_data='save')
    go_back = types.InlineKeyboardButton('Назад', callback_data='CFin')
    markup.add(*[save, go_back])
    if value_holder.who == 1:
        await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
                                    message_id=value_holder.message_id_holder,
                                    text=f'Выбранный филиал - {selectors.filial_reversed[str(value_holder.filial)]}\n'
                                         f'Вы - {selectors.who[str(value_holder.who)]}\n'
                                         f'Выбранный факультет - {selectors.faculty_reversed[str(value_holder.faculty)]}\n'
                                         f'Выбранный курс - {selectors.course_chair_reversed[str(value_holder.course)]}\n'
                                         f'Выбранная группа - {selectors.groups_teachers_reversed[str(value_holder.group)]}',
                                    reply_markup=markup
                                    )
    else:
        await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
                                    message_id=value_holder.message_id_holder,
                                    text=f'Выбранный филиал - {selectors.filial_reversed[str(value_holder.filial)]}\n'
                                         f'Вы - {selectors.who[str(value_holder.who)]}\n'
                                         f'Выбранный факультет - {selectors.faculty_reversed[str(value_holder.faculty)]}\n'
                                         f'Выбранная кафедра - {selectors.course_chair_reversed[str(value_holder.chair)]}\n'
                                         f'Выбранный преподаватель - {selectors.groups_teachers_reversed[str(value_holder.teacher)]}',
                                    reply_markup=markup
                                    )


@dp.callback_query_handler(lambda call: call.data.startswith('save'))
async def final_confirm(call):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    today = types.KeyboardButton('Расписание сегодня')
    markup.add(today)
    await bot.delete_message(chat_id=value_holder.chat_id_holder,
                             message_id=value_holder.message_id_holder)
    await bot.send_message(chat_id=value_holder.chat_id_holder,
                           text=f'Успешно сохранено',
                           reply_markup=markup
                           )

    # if value_holder.who == 1:
    #     await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
    #                                 message_id=value_holder.message_id_holder,
    #                                 text=f'Выбранный филиал - {selectors.filial_reversed[str(value_holder.filial)]}\n'
    #                                      f'Вы - {selectors.who[str(value_holder.who)]}\n'
    #                                      f'Выбранный факультет - {selectors.faculty_reversed[str(value_holder.faculty)]}\n'
    #                                      f'Выбранный курс - {selectors.course_chair_reversed[str(value_holder.course)]}\n'
    #                                      f'Выбранная группа - {selectors.groups_teachers_reversed[str(value_holder.group)]}',
    #                                 reply_markup=markup
    #                                 )
    # else:
    #     await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
    #                                 message_id=value_holder.message_id_holder,
    #                                 text=f'Выбранный филиал - {selectors.filial_reversed[str(value_holder.filial)]}\n'
    #                                      f'Вы - {selectors.who[str(value_holder.who)]}\n'
    #                                      f'Выбранный факультет - {selectors.faculty_reversed[str(value_holder.faculty)]}\n'
    #                                      f'Выбранная кафедра - {selectors.course_chair_reversed[str(value_holder.chair)]}\n'
    #                                      f'Выбранный преподаватель - {selectors.groups_teachers_reversed[str(value_holder.teacher)]}',
    #                                 reply_markup=markup
    #                                 )


# Callback handlers for back operation
@dp.callback_query_handler(lambda call: call.data.startswith('cFilial'))
async def process_to_filial_back(call: types.CallbackQuery):
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


@dp.callback_query_handler(lambda call: call.data.startswith('cFacult'))
async def process_to_who_back(call: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup()
    student = types.InlineKeyboardButton('Студент', callback_data='who_student')
    teacher = types.InlineKeyboardButton('Преподаватель', callback_data='who_teacher')
    cancel = types.InlineKeyboardButton('Назад', callback_data='cFilial')
    value_holder.who = None
    markup.add(*[student, teacher, cancel])
    await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
                                message_id=value_holder.message_id_holder,
                                text=f'Выбранный филиал - {selectors.filial_reversed[str(value_holder.filial)]}\n'
                                     f'Выберите студент вы или преподаватель',
                                reply_markup=markup
                                )


@dp.callback_query_handler(lambda call: call.data.startswith('cCChair'))
async def process_to_faculty_back(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    items = choose_faculty()
    markup.add(*items)
    selectors.course_chair = None
    selectors.course_chair_reversed = None
    value_holder.faculty = None
    await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
                                message_id=value_holder.message_id_holder,
                                text=f'Выбранный филиал - {selectors.filial_reversed[str(value_holder.filial)]}\n'
                                     f'Вы - {selectors.who[str(value_holder.who)]}\n'
                                     f'Выберите факультет:',
                                reply_markup=markup
                                )


@dp.callback_query_handler(lambda call: call.data.startswith('cGcall'))
async def process_to_course_back(call: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_width=1)
    items = choose_course_chair()
    markup.add(*items)
    value_holder.course = None
    value_holder.chair = None
    selectors.groups_teachers = None
    selectors.groups_teachers_reversed = None
    if value_holder.who == 1:
        await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
                                    message_id=value_holder.message_id_holder,
                                    text=f'Выбранный филиал - {selectors.filial_reversed[str(value_holder.filial)]}\n'
                                         f'Вы - {selectors.who[str(value_holder.who)]}\n'
                                         f'Выбранный факультет - {selectors.faculty_reversed[str(value_holder.faculty)]}\n'
                                         f'Выберите курс:',
                                    reply_markup=markup
                                    )
    else:
        await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
                                    message_id=value_holder.message_id_holder,
                                    text=f'Выбранный филиал - {selectors.filial_reversed[str(value_holder.filial)]}\n'
                                         f'Вы - {selectors.who[str(value_holder.who)]}\n'
                                         f'Выбранный факультет - {selectors.faculty_reversed[str(value_holder.faculty)]}\n'
                                         f'Выберите кафедру:',
                                    reply_markup=markup
                                    )


@dp.callback_query_handler(lambda call: call.data.startswith('CFin'))
async def process_to_course_back(call: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_width=2)
    items = choose_group_teacher()
    markup.add(*items)
    value_holder.group = None
    value_holder.teacher = None
    if value_holder.who == 1:
        await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
                                    message_id=value_holder.message_id_holder,
                                    text=f'Выбранный филиал - {selectors.filial_reversed[str(value_holder.filial)]}\n'
                                         f'Вы - {selectors.who[str(value_holder.who)]}\n'
                                         f'Выбранный факультет - {selectors.faculty_reversed[str(value_holder.faculty)]}\n'
                                         f'Выберите курс:',
                                    reply_markup=markup
                                    )
    else:
        await bot.edit_message_text(chat_id=value_holder.chat_id_holder,
                                    message_id=value_holder.message_id_holder,
                                    text=f'Выбранный филиал - {selectors.filial_reversed[str(value_holder.filial)]}\n'
                                         f'Вы - {selectors.who[str(value_holder.who)]}\n'
                                         f'Выбранный факультет - {selectors.faculty_reversed[str(value_holder.faculty)]}\n'
                                         f'Выберите кафедру:',
                                    reply_markup=markup
                                    )

# @dp.callback_query_handler(lambda call: call.data.startswith('type_'))
# async def choose_faculty(call: types.CallbackQuery):
#     await bot.send_message(call.message.chat.id,
#                            f"Вы выбрали {'студент' if call.data == 'type_student' else 'преподаватель'}")
#
#
# @dp.message_handler()
# async def echo_message(msg: types.Message):
#     await bot.send_message(msg.from_user.id, msg.text + f' {msg.from_user.id}')


if __name__ == '__main__':
    executor.start_polling(dp)
