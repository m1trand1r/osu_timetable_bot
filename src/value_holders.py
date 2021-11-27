class Student:
    def __init__(self):

        self._faculty = None
        self._course = None
        self._group = None


class Teacher:
    def __init__(self):
        self.faculty = None
        self.chair = None
        self.teacher = None


class ValueHolder:
    def __init__(self):
        self.chat_id_holder = None
        self.message_id_holder = None
        self.filial = None
        self.client = None
        self.who = None

    def set_who(self, who: int):
        self.who = who
        if who == 1:
            self.client = Student()
        else:
            self.client = Teacher()


class SelectorsHolder:
    def __init__(self):
        self.filial, self.filial_reversed = None, None
        self.faculty, self.faculty_reversed = None, None
        self.who_reversed = {'student': 1, 'teacher': 2}
        self.course, self.course_reversed = None, None
        self.groups, self.groups_reversed = None, None
        self.teacher, self.teacher_reversed = None, None
