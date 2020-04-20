class Course:
    def __init__(self, id="", name="", mark="", type="", host="", credit="", hours="", district="", teacher="",
                 time_and_loc="",
                 comments=""):
        self.id = id
        self.name = name
        self.mark = mark
        self.type = type
        self.host = host
        self.credit = credit
        self.teacher = teacher
        self.hours = hours
        self.district = district
        self.time_and_loc = time_and_loc
        self.comments = comments

    def __str__(self):
        s = "课程信息("
        attributes = [x for x in dir(self) if not x.startswith("__")]
        for attr in attributes:
            if getattr(self, attr) is not None and len(getattr(self, attr)) > 0:
                if len(s) > 5:
                    s += ";"
                s += attr + ":" + str(getattr(self, attr))
        s += ')'
        return s
