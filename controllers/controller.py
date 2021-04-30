from random import shuffle
from models import match, player, round, tournament
from views import view
from tinydb import TinyDB


class Controller:
    def __init__(self):
        self.view = view.View()
        self.db = TinyDB("./db.json")

    def choice(self):
        choice = int(input("What is your choice ? "))
        return choice

    def add_player(self):
        players = []
        for i in range(8):
            name_player = input("Enter player's name: ")
            players.append(player.Player(first_name=name_player))
        return players

    def order_players_by_rank(self, players: list) -> list:
        return sorted(players, key=lambda x: x.rank, reverse=True)

    def order_players_by_point(self, players: list) -> list:
        return sorted(players, key=lambda x: x.point, reverse=True)

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

    def match(self, pair):
        winner = input("Who's the winner ? ")
        if winner == pair[0].first_name:
            pair[0].point += 1
        elif winner == pair[1].first_name:
            pair[1].point += 1
        else:
            pair[0].point += 0.5
            pair[1].point += 0.5

    def first_round(self, players, tournament):
        players = self.order_players_by_rank(players)
        pairs = self.get_pairs_by_rank(players)
        tournament.matches.extend(pairs)
        print({i: pair for i, pair in enumerate(pairs, 0)})
        choice = int(input("Which match has been played ? "))
        self.match(pairs[choice])
        tournament.number_of_matches += 1
        self.view.display_players(players)
        self.view.display_points(players)
        tournament.number_of_turns -= 1
        self.view.display_left_rounds(tournament.number_of_turns)

    def play_a_round(self, players, tournament):
        if tournament.number_of_turns > 0:
            players = self.order_players_by_point(players)
            pairs = self.get_pairs_by_point(players, tournament.matches)
            tournament.matches.extend(pairs)
            print({i: pair for i, pair in enumerate(pairs, 0)})
            choice = int(input("Which match has been played ? "))
            self.match(pairs[choice])
            tournament.number_of_matches += 1
            self.view.display_players(players)
            self.view.display_points(players)
            tournament.number_of_turns -= 1
            self.view.display_left_rounds(tournament.number_of_turns)

    def save_tournaments(self, tournaments):
        serialized_tournaments = []
        for tournament in tournaments:
            serialized_tournament = {
                "name": tournament.name,
                "location": tournament.location,
                "date": tournament.date,
                "number_of_turns": tournament.number_of_turns,
                "rounds": tournament.rounds,
                "players": tournament.players,
                "time_control": tournament.time_control,
                "description": tournament.description,
                "matches": tournament.matches
            }
            serialized_tournaments.append(serialized_tournament)
        tournament_table = self.db.table("tournaments")
        tournament_table.truncate()
        tournament_table.insert_multiple(serialized_tournaments)

    def save_players(self, players):
        serialized_players = []
        for player in players:
            serialized_player = {
                "first_name": player.first_name,
                "last_name": player.last_name,
                "birth": player.birth,
                "gender": player.gender,
                "rank": player.rank,
                "point": player.point
            }
            serialized_players.append(serialized_player)
        players_table = self.db.table('players')
        players_table.truncate()
        players_table.insert_multiple(serialized_players)
