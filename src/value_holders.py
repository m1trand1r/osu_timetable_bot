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
        self.client = None
        self.who = None

    def set_who(self, who: int):
        self.who = who
        if who == 1:
            self.client = Student()
        else:
            self.client = Teacher()