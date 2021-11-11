from aiogram.dispatcher.filters.state import State, StatesGroup


class StudentProcessor(StatesGroup):
    type_worker = State()
    faculty = State()
    course = State()
    group = State()


class TeacherProcessor(StatesGroup):
    type_worker = State()
    faculty = State()
    chair = State()
    teacher = State()


