# from tinydb import TinyDB
#
# db = TinyDB("db.json")


class Player:
    def __init__(self, first_name, last_name=None, birth=None, gender=None, rank=0, point=0):
        self.first_name = first_name
        self.last_name = last_name
        self.birth = birth
        self.gender = gender
        self.rank = rank
        self.point = point

    def __repr__(self):
        return self.first_name

    # def save_in_db(self):
    #     serialized_player = {
    #         "first_name": self.first_name,
    #         "last_name": self.last_name,
    #         "birth": self.birth,
    #         "gender": self.gender,
    #         "rank": self.rank,
    #         "point": self.point
    #     }
    #     players_table = db.table('players')
    #     players_table.truncate()
    #     players_table.insert(serialized_player)
