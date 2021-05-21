from datetime import datetime
from enum import Enum
from json import dumps, loads
from random import shuffle

from tinydb import TinyDB, where
from tinydb.operations import add

from utils.utils import flatten_list, order_players_by_key

db = TinyDB("db.json")


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
        serialized_player = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth": self.birth,
            "gender": self.gender,
            "rank": self.rank,
            "point": self.point
        }
        players_table = db.table('players')
        players_table.insert(serialized_player)

    def get_document_from_instance(self):
        players_table = db.table('players')
        for player in players_table.all():
            if player['first_name'] == self.first_name and player['last_name'] == self.last_name:
                return player


class Tournament:
    def __init__(self, name, location=None, date=None, rounds=None, players=None, matches=None, description=None,
                 time_control=None,
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

    @property
    def len_players(self):
        return len(self.players)

    def __repr__(self):
        return self.name

    def save_in_db(self):
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
        }
        tournaments_table = db.table('tournaments')
        tournaments_table.insert(serialized_tournament)

    def add_player_in_tournament(self, player, tournament_name):
        db.table('tournaments').update(
            add("players", [player.doc_id]),
            where('name') == tournament_name
        )


class Round:
    def __init__(self, tournament_choice):
        self.tournament_choice = tournament_choice
        self.tournament = db.table('tournaments').get(where('name') == tournament_choice)
        self.start_time = datetime.now().isoformat()
        self.round_number = len(db.table('tournaments').get(where('name') == tournament_choice)['rounds'])
        self.players = [i for i in db.table('players').all() if i.doc_id in self.tournament['players']]
        self.round_done = False

    @property
    def end_date(self):
        if self.round_done:
            return datetime.now().isoformat()

    def get_pairs_by_rank(self, players: list) -> list:
        pairs_list = []
        list_one = players[:4]
        list_two = players[4:]
        for i, j in zip(list_one, list_two):
            pairs_list.append((i, j))

        return pairs_list

    def get_pairs_by_point(self, players: list, played_pairs: list) -> list:
        pairs_list = []
        ref_list = []

        for i in players:
            for j in players:
                if i != j and ((i, j) not in played_pairs and (
                        j, i) not in played_pairs) and (
                        (i, j) not in pairs_list and (
                        j, i) not in pairs_list) and i not in ref_list and j not in ref_list:
                    pairs_list.append((i, j))
                    ref_list.append(i)
                    ref_list.append(j)

        return pairs_list

    def get_pairs(self, players: list) -> list:
        pairs_list = []
        shuffle(players)
        for i in range(0, len(players), 2):
            pairs_list.append(players[i:i + 2])
        return pairs_list

    def sorted_players(self, players: list):
        if self.round_number == 1:
            return order_players_by_key(players, 'rank')
        return order_players_by_key(players, 'point')

    def sorted_pairs(self, players: list):
        players = self.sorted_players(players)
        if self.round_number == 1:
            return [(i[0].doc_id, i[1].doc_id) for i in self.get_pairs_by_rank(players)]
        return [(i[0].doc_id, i[1].doc_id) for i in self.get_pairs_by_point(players, self.get_pairs(players))]

    def save_pairs_in_db(self, tournament_choice, pairs):
        db.table('tournaments').update(
            add("rounds", [{self.round_number + 1: pairs}]),
            where('name') == tournament_choice
        )

    def add_matches_in_tournament(self, pairs: list, tournament_name):
        db.table('tournaments').update(
            add('matches', [pairs]),
            where('name') == tournament_name
        )

    def winner_match(self, winner_id):
        winner = db.table('players').get(doc_id=winner_id)
        db.table('players').update(
            add('point', 1),
            doc_ids=[winner.doc_id])

    def draw_match(self, pair):
        player_one_doc = db.table('players').get(doc_id=pair[0])
        player_two_doc = db.table('players').get(doc_id=pair[1])
        pair_ids = [player_one_doc.doc_id, player_two_doc.doc_id]
        db.table('players').update(
            add('point', 0.5),
            doc_ids=pair_ids)

    def matches_not_played(self, pairs: list) -> list:
        matches_not_played = []
        for pair in pairs:
            if pair not in self.tournament['matches']:
                matches_not_played.append(pair)
        return matches_not_played

    def get_name_from_ids(self, pair):
        pair = flatten_list(pair)
        return [{player.doc_id: f"{player['first_name']} {player['last_name']}"} for player in db.table('players') if
                player.doc_id in pair]


class Database:
    def __init__(self):
        self.tournaments = db.table('tournaments')
        self.players = db.table('players')

    def get_report(self, choice_number, tournament_name=None):
        if choice_number == 1:
            return self.players_alpha_report()
        elif choice_number == 2:
            return self.players_ranking_report()
        elif choice_number == 3:
            return self.players_alpha_report(tournament_name)
        elif choice_number == 4:
            return self.players_ranking_report(tournament_name)
        elif choice_number == 5:
            return self.get_all_tournaments()
        elif choice_number == 6:
            return self.get_rounds_of_tournament(tournament_name)
        elif choice_number == 7:
            return self.get_matches_of_tournament(tournament_name)

    def load_player_data(self) -> list:
        player_table = db.table("players")
        return [Player(**player) for player in player_table.all()]

    def load_tournament_data(self) -> list:
        tournament_table = db.table("tournaments")
        return [Tournament(**tournament) for tournament in tournament_table.all()]

    def players_alpha_report(self, tournament=None):
        '''
        assure all players have a last name
        '''
        if tournament is not None:
            tournament_players = self.tournaments.get(where('name') == tournament)['players']
            players = [Player(**player) for player in self.players if player.doc_id in tournament_players]
        else:
            players = self.load_player_data()

        for player in sorted(players, key=lambda x: x.first_name):
            print({'first_name': player.first_name, 'last_name': player.last_name, 'point': player.point})

    def players_ranking_report(self, tournament=None):
        if tournament is not None:
            tournament_players = self.tournaments.get(where('name') == tournament)['players']
            players = [Player(**player) for player in self.players if player.doc_id in tournament_players]
        else:
            players = self.load_player_data()

        for player in sorted(players, key=lambda x: x.rank, reverse=True):
            print({'first_name': player.first_name, 'last_name': player.last_name, 'ranking': player.rank})

    def get_all_tournaments(self):
        for tournament in self.load_tournament_data():
            print({'name': tournament})

    def get_rounds_of_tournament(self, tournament_name=None):
        tournaments_table = db.table('tournaments')
        tournaments = loads(dumps(tournaments_table.all()))
        for tournament in tournaments:
            if tournament['name'] == tournament_name:
                print(tournament['rounds'])

    def get_matches_of_tournament(self, tournament_name=None):
        tournaments_table = db.table('tournaments')
        tournaments = loads(dumps(tournaments_table.all()))
        for tournament in tournaments:
            if tournament['name'] == tournament_name:
                print(tournament['matches'])


class Match:
    def __init__(self, pair, result):
        self.pair = pair
        self.result = result
