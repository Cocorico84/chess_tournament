from datetime import datetime


class Round:
    def __init__(self, name):
        self.name = name
        self.start_time = datetime.now()
        self.round_done = False

    @property
    def end_date(self):
        if self.round_done:
            return datetime.now()
