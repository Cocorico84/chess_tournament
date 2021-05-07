from random import shuffle

from models import Tournament, Player, Round, Database
from utils.menu import Menu
from view import HomeMenuView, TournamentView, PlayerView, MatchView, QuitView, ReportView


class ApplicationController:
    def __init__(self):
        self.controllers = []

    def start(self):
        self.controller = HomeMenuController()
        while self.controller:
            self.controller = self.controller()
            self.controllers.append(self.controller)


class HomeMenuController:
    def __init__(self):
        self.menu = Menu()
        self.view = HomeMenuView(self.menu)

    def __call__(self):
        self.menu.add("auto", "create a tournament", CreateTournamentController())
        self.menu.add("auto", "add a player", AddPlayerController())
        self.menu.add("auto", "launch round", LaunchRoundController())
        self.menu.add("auto", "write a match result", MatchResultController())
        self.menu.add("auto", "get a report", ReportController())
        self.menu.add("auto", "save", SaveController())
        self.menu.add("q", "quit", QuitController())

        user_choice = self.view.get_user_choice()

        return user_choice.handler


class CreateTournamentController:
    def __init__(self):
        self.tournament_view = TournamentView()

    def __call__(self):
        tournament = Tournament(self.tournament_view.get_info())
        tournament.save_in_db()
        return HomeMenuController()


class AddPlayerController:
    def __init__(self):
        self.player_view = PlayerView()

    def __call__(self):
        player = Player(self.player_view.get_info())
        player.save_in_db()
        return HomeMenuController()


class LaunchRoundController:
    def __init__(self):
        self.tournament = Database().load_tournament_data()[0]
        self.match = MatchResultController()

    def __call__(self):
        round = Round(name=f"Round {len(self.tournament.rounds) + 1}")
        self.tournament.rounds.append(round)
        return HomeMenuController


class MatchResultController:
    def __init__(self):
        self.match_view = MatchView()
        self.players = Database().load_player_data()

    def __call__(self):
        players = self.order_players_by_rank(self.players) if round == 1 else self.order_players_by_point(self.players)
        pairs = self.get_pairs_by_rank(self.players) if round == 1 else self.get_pairs_by_point(players, self.get_pairs(self.players))

        self.match_view._display_matches(pairs)
        pair = self.match_view.get_match_played()
        winner = self.match_view.get_the_winner()
        self.match(pairs[pair], winner)
        return HomeMenuController

    def match(self, pair, winner):
        if winner == pair[0].first_name:
            pair[0].point += 1
        elif winner == pair[1].first_name:
            pair[1].point += 1
        else:
            pair[0].point += 0.5
            pair[1].point += 0.5

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

    # def play_round(self, players, tournament, round):

    #     tournament.matches.extend(pairs)
    #     self.match.match(pairs[choice], self.winner)
    #     tournament.number_of_matches += 1
    #     # self.report.players_alpha_report(players, self.tournament)
    #     tournament.number_of_turns -= 1
    #     # self.report.get_rounds_of_tournament()


class ReportController:
    def __init__(self):
        self.report_view = ReportView()
        self.players = []
        self.db = Database()

    def __call__(self):
        choice = self.report_view.report_choice()
        self.report_view._choices[int(choice)][1](self.db)
        return HomeMenuController


class SaveController:
    def __int__(self):
        self.players = Database().load_player_data()
        self.tournaments = Database().load_tournament_data()

    def __call__(self):
        for player in self.players:
            player.save_in_db()

        for tournament in self.tournaments:
            tournament.save_in_db()
        return HomeMenuController


class QuitController:
    def __init__(self):
        self.quit_view = QuitView()

    def __call__(self):
        self.quit_view()
