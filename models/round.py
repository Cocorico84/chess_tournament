from datetime import datetime


class Round:
    def __init__(self, name, date, end_time):
        self.name = name
        self.date = date
        self.start_time = datetime.now()
        self.end_time = end_time
