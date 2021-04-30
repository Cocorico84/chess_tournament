from tinydb import TinyDB


class Database:
    def __init__(self):
        self.db = TinyDB('../db.json')

    def load_data(self):
        print(self.db.all())
