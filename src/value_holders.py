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
        self.who = None
        self.faculty = None
        self.course = None
        self.group = None
        self.chair = None
        self.teacher = None


class SelectorsHolder:
    def __init__(self):
        self.filial, self.filial_reversed = None, None
        self.faculty, self.faculty_reversed = None, None
        self.who, self.who_reversed = {'1': 'student', '2': 'teacher'}, {'student': 1, 'teacher': 2}
        self.course_chair, self.course_chair_reversed = None, None
        self.groups, self.groups_reversed = None, None
        self.teacher, self.teacher_reversed = None, None
