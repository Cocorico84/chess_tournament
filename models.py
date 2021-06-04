from datetime import datetime
from json import dumps, loads
from random import shuffle

from tinydb import TinyDB, where
from tinydb.operations import add, set

from utils.utils import order_players_by_key

db = TinyDB("db.json")


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

    def update_rank(self, rank: int):
        """
        This method allows to change arbitrary the rank of the player
        :param rank: choose the rank you want to give for the player
        :type rank: int

        """
        players_table = db.table('players')
        player = self.get_document_from_instance()
        players_table.update(
            set('rank', rank),
            doc_ids=[player.doc_id]
        )


class Tournament:
    def __init__(self, name, location=None, date=None, rounds=None, players=None, matches=None, description=None,
                 time_control=None, history=None, round_info=None, is_active=False,
                 number_of_turns=4):
        self.name = name
        self.location = location
        self.date = datetime.now().isoformat() if date is not None else ""
        self.number_of_turns = number_of_turns
        self.rounds = rounds if rounds is not None else []
        self.players = players if players is not None else []
        self.time_control = time_control
        self.description = description
        self.matches = matches if matches is not None else []
        self.history = history if history is not None else []
        self.round_info = round_info if round_info is not None else []
        self.number_of_players = len(self.players)
        self.is_active = is_active

    def __repr__(self):
        return self.name

    def save_in_db(self):
        """
        This function serialize our data et save it in the database
        """
        self.is_active = True
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
            "history": self.history,
            "round_info": self.round_info,
            "is_active": self.is_active,
        }
        tournaments_table = db.table('tournaments')
        tournaments_table.insert(serialized_tournament)

    def add_player_in_tournament(self, player, tournament_name):
        db.table('tournaments').update(
            add("players", [player.doc_id]),
            where('name') == tournament_name
        )

    def get_players_from_tournament(self) -> list:
        """
        Search all players in the table 'players' who are in the active tournament
        """
        return [i for i in db.table('players').all() if i.doc_id in self.players]

    def create_round(self):
        self.round_info.append(Round(round_number=len(self.rounds) + 1).serialize())
        db.table('tournaments').update(
            add('round_info', [self.round_info[-1]]),
            where('name') == self.name
        )

    def update_end_round(self):
        """
        Add the end date of the round and update it in the database
        """
        round = db.table("tournaments").get(where('name') == self.name)['round_info'][-1]
        instance_round = Round(**round)
        instance_round.end_date = datetime.now().isoformat()
        serialize_round = instance_round.serialize()
        db.table('tournaments').update(
            add('round_info', [serialize_round]),
            where('name') == self.name
        )

    def create_match(self, pair, winner):
        self.history.append(Match(pair=pair, winner=winner).serialize())
        db.table('tournaments').update(
            add('history', [self.history[-1]]),
            where('name') == self.name
        )

        self.matches.append(Match().serialize())

    def get_pairs_by_rank(self, players: list) -> list:
        """
        Split the list of the 8 players in half and make pairs with one of each list
        :param players:
        """
        pairs_list = []
        list_one = players[:4]
        list_two = players[4:]
        for i, j in zip(list_one, list_two):
            pairs_list.append((i, j))

        return pairs_list

    def get_pairs_by_point(self, players: list, played_pairs: list) -> list:
        """
        This algorithm makes pairs in using once each player during the round and make pairs not already made.
        :param played_pairs: list of pairs already played
        """
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
        """
        Make pairs randomly
        """
        pairs_list = []
        shuffle(players)
        for i in range(0, len(players), 2):
            pairs_list.append(players[i:i + 2])
        return pairs_list

    def sorted_players(self, players: list):
        """
        Sort players depending on the round. If it is the round number 1 , players are sorted by rank otherwise
        players are sorted by points
        """
        if len(self.rounds) == 1:
            return order_players_by_key(players, 'rank')
        return order_players_by_key(players, 'point')

    def sorted_pairs(self, players: list):
        """
        Sort players by pairs with their doc_id
        :param players:
        :type players:
        :return:
        """
        players = self.sorted_players(players)
        if len(self.rounds) == 1:
            return [(i[0].doc_id, i[1].doc_id) for i in self.get_pairs_by_rank(players)]
        return [(i[0].doc_id, i[1].doc_id) for i in self.get_pairs_by_point(players, self.get_pairs(players))]

    def save_pairs_in_db(self, pairs):
        db.table('tournaments').update(
            add("rounds", [{len(self.rounds) + 1: pairs}]),
            where('name') == self.name
        )

    def add_matches_in_tournament(self, pairs: list):
        db.table('tournaments').update(
            add('matches', [pairs]),
            where('name') == self.name
        )

    def winner_match(self, winner_id):
        """
        Add 1 point  to the winner of the match
        """
        winner = db.table('players').get(doc_id=winner_id)
        db.table('players').update(
            add('point', 1),
            doc_ids=[winner.doc_id])

    def draw_match(self, pair):
        """
        Add 0.5 point for each player in the pair
        """
        player_one_doc = db.table('players').get(doc_id=pair[0])
        player_two_doc = db.table('players').get(doc_id=pair[1])
        pair_ids = [player_one_doc.doc_id, player_two_doc.doc_id]
        db.table('players').update(
            add('point', 0.5),
            doc_ids=pair_ids)

    def matches_not_played(self, pairs: list) -> list:
        """
        Compare a list of pairs of the round and remove all pairs played in another list
        """
        matches_not_played = []
        for pair in pairs:
            if pair not in self.matches:
                matches_not_played.append(pair)
        return matches_not_played

    def get_name_from_ids(self, pairs: list) -> list:
        """
        :type pairs: a list of pairs with doc_id only
        :return: a list of pairs with the first name and last name from the player
        """
        pairs_with_names = []
        for pair in pairs:
            pairs_with_names.append(
                [{player.doc_id: f"{player['first_name']} {player['last_name']}"} for player in db.table('players') if
                 player.doc_id in pair])
        return pairs_with_names


class Round:
    def __init__(self, start_time=datetime.now().isoformat(), round_number=0, end_date=0):
        self.start_time = start_time
        self.round_number = round_number
        self.end_date = end_date

    def serialize(self):
        return {
            "start_time": self.start_time,
            "round_number": self.round_number,
            "end_date": self.end_date
        }


class Database:
    def __init__(self):
        self.tournaments = db.table('tournaments')
        self.players = db.table('players')

    def all_tournaments_in_progress(self):
        return [Tournament(**tournament) for tournament in self.tournaments.all() if tournament['is_active']]

    def load_player_data(self) -> list:
        """
        :return: list of all player instances
        """
        player_table = db.table("players")
        return [Player(**player) for player in player_table.all()]

    def load_tournament_data(self) -> list:
        """
        :return: list of all tournament instances
        """
        tournament_table = db.table("tournaments")
        return [Tournament(**tournament) for tournament in tournament_table.all()]

    def players_alpha_report(self, tournament: str = None) -> list:
        '''
        required: assure all players have a last name
        :return: list of all player instances of a specific tournament in alphabetial order
        '''
        alpha_players = []
        if tournament is not None:
            tournament_players = self.tournaments.get(where('name') == tournament)['players']
            players = [Player(**player) for player in self.players if player.doc_id in tournament_players]
        else:
            players = self.load_player_data()

        for player in sorted(players, key=lambda x: x.last_name):
            alpha_players.append(player)

        return alpha_players

    def players_ranking_report(self, tournament: str = None):
        """
        :return: list of all player instances of a specific tournament sorted by rank
        """
        ranked_players = []
        if tournament is not None:
            tournament_players = self.tournaments.get(where('name') == tournament)['players']
            players = [Player(**player) for player in self.players if player.doc_id in tournament_players]
        else:
            players = self.load_player_data()

        for player in sorted(players, key=lambda x: x.rank, reverse=True):
            ranked_players.append(player)

        return ranked_players

    def get_all_tournaments(self) -> list:
        """
        :return: list of all tournament instances (played or still active)
        """
        return [tournament for tournament in self.load_tournament_data()]

    def get_rounds_of_tournament(self, tournament_name: str = None) -> list:
        """
        :return: list of all rounds (played and in progress) of a specific tournament

        """
        tournaments_table = db.table('tournaments')
        tournaments = loads(dumps(tournaments_table.all()))
        for tournament in tournaments:
            if tournament['name'] == tournament_name:
                return tournament['rounds']

    def get_matches_of_tournament(self, tournament_name: str = None) -> list:
        """
        :return: list of all played matches of a specific tournament
        """
        tournaments_table = db.table('tournaments')
        tournaments = loads(dumps(tournaments_table.all()))
        for tournament in tournaments:
            if tournament['name'] == tournament_name:
                return tournament['history']


class Match:
    def __init__(self, pair=None, winner=""):
        self.pair = pair
        self.winner = winner

    def serialize(self):
        return {
            "pair": self.pair,
            "winner": self.winner
        }
