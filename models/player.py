class Player:
    def __init__(self, first_name, last_name=None, birth=None, gender=None, rank=0, point=0):
        self.first_name = first_name
        self.last_name = last_name
        self.birth = birth
        self.gender = gender
        self.rank = rank
        self.point = point
        # self.opponents = []

    def __repr__(self):
        return self.first_name
