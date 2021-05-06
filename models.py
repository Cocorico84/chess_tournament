from tinydb import TinyDB
from enum import Enum
from datetime import datetime


class TimeControl(Enum):
    Bullet = 1
    Blitz = 2
    Rapid = 3


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

    def save_in_db(self):
        db = Database().db
        serialized_player = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth": self.birth,
            "gender": self.gender,
            "rank": self.rank,
            "point": self.point
        }
        players_table = db.table('players')
        players_table.truncate()
        players_table.insert(serialized_player)


class Tournament:
    def __init__(self, name, location=None, description=None, time_control=None,
                 number_of_turns=4):
        self.name = name
        self.location = location
        self.date = datetime.now().isoformat()
        self.number_of_turns = number_of_turns
        self.rounds = []
        self.players = []
        self.time_control = time_control
        self.description = description
        self.matches = []
        self.number_of_matches = 0

    def save_in_db(self):
        db = Database().db
        serialized_tournament = {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "number_of_turns": self.number_of_turns,
            "rounds": self.rounds,
            "players": self.players,
            "time_control": self.time_control,
            "description": self.description,
            "matches": self.matches,
            "number_of_matches": self.number_of_matches
        }
        tournaments_table = db.table('tournaments')
        tournaments_table.truncate()
        tournaments_table.insert(serialized_tournament)


class Round:
    def __init__(self, name):
        self.name = name
        self.start_time = datetime.now().isoformat()
        self.round_done = False

    @property
    def end_date(self):
        if self.round_done:
            return datetime.now().isoformat()


class Database:
    def __init__(self):
        self.db = TinyDB('db.json')

    def load_player_data(self):
        player_table = self.db.table("players")
        return player_table.all()

    def load_tournament_data(self):
        tournament_table = self.db.table("tournaments")
        return tournament_table.all()


class Match:
    def __init__(self, pair, result):
        self.pair = pair
        self.result = result
