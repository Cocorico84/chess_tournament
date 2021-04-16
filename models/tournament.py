from enum import Enum


class TimeControl(Enum):
    Bullet = 1
    Blitz = 2
    Rapid = 3


class Tournament:
    def __init__(self, name, location=None, date=None, rounds=None, players=None, description=None, number_of_turns=4):
        self.name = name
        self.location = location
        self.date = date
        self.number_of_turns = number_of_turns
        self.rounds = rounds
        self.players = players
        self.time_control = TimeControl
        self.description = description

    @property
    def turn(self):
        return self.rounds + 1
