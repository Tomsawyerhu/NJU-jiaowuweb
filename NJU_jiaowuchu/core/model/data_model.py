class Course:
    def __init__(self, id=None, name=None, mark=None, type=None, credit=None, teacher=None, time_and_loc=None,
                 comments=None):
        self.id = id
        self.name = name
        self.mark = mark
        self.type = type
        self.credit = credit
        self.teacher = teacher
        self.time_and_loc = time_and_loc
        self.comments = comments