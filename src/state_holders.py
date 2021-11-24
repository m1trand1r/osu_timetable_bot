from aiogram.dispatcher.filters.state import State, StatesGroup
#
#
# class StudentProcessor(StatesGroup):
#     # type_worker = State()
#     # faculty = State()
#     course = State()
#     group = State()
#
#
# class TeacherProcessor(StatesGroup):
#     # type_worker = State()
#     # faculty = State()
#     chair = State()
#     teacher = State()


class StateHolder:
    def __init__(self):
        self.type_worker = State()
        self.faculty = State()
        self.course = State()
        self.final_name = State()



