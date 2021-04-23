from enum import Enum
from datetime import datetime


class TimeControl(Enum):
    Bullet = 1
    Blitz = 2
    Rapid = 3


class Tournament:
    def __init__(self, name, location=None, players=None, description=None, time_control=None,
                 number_of_turns=4):
        self.name = name
        self.location = location
        self.date = datetime.now()
        self.number_of_turns = number_of_turns
        self.rounds = []
        self.players = players
        self.time_control = time_control
        self.description = description
        self.matches = []
