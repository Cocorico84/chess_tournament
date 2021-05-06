from utils.menu import Menu
from view import HomeMenuView, TournamentView, PlayerView, RoundView, MatchView, QuitView, ReportView
from models import Tournament, Player, Round
from random import shuffle


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
        self.tournaments = []

    def __call__(self):
        self.tournaments.append(Tournament(self.tournament_view.get_info()))
        return HomeMenuController()


class AddPlayerController:
    def __init__(self):
        self.player_view = PlayerView()
        self.players = []

    def __call__(self):
        self.players.append(Player(self.player_view.get_info()))
        return HomeMenuController()

    def order_players_by_rank(self, players: list) -> list:
        return sorted(players, key=lambda x: x.rank, reverse=True)

    def order_players_by_point(self, players: list) -> list:
        return sorted(players, key=lambda x: x.point, reverse=True)


class LaunchRoundController:
    def __init__(self):
        self.round_view = RoundView()
        self.players = AddPlayerController().players
        self.player = AddPlayerController()
        if len(CreateTournamentController().tournaments) > 0:
            self.tournament = CreateTournamentController().tournaments[0]
        else:
            self.tournament = None
        self.match = MatchResultController()

    def __call__(self):
        if len(self.players) == 8:
            if len(self.tournament.rounds) < 4:
                chess_round = Round(name=f"Round {len(self.tournament.rounds) + 1}")
                self.tournament.rounds.append(chess_round)
        return HomeMenuController



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

    def play_round(self, players, tournament, round):
        players = self.player.order_players_by_rank(players) if round == 1 else self.player.order_players_by_point(players)
        pairs = self.get_pairs_by_rank(players) if round == 1 else self.get_pairs_by_point(players)

        self.tournament.matches.extend(pairs)
        self.round_view._display_matches()

        choice = self.round_view.get_match_played()
        self.match(pairs[choice])
        tournament.number_of_matches += 1
        # display players and rank
        tournament.number_of_turns -= 1
        # display left rounds


class MatchResultController:
    def __init__(self):
        self.match_view = MatchView()
        self.pairs = None

    def __call__(self):
        winner = self.match_view.get_the_winner(self.pair)
        self.match(self.pair, winner)
        return HomeMenuController

    def match(self, pair, winner):
        if winner == pair[0].first_name:
            pair[0].point += 1
        elif winner == pair[1].first_name:
            pair[1].point += 1
        else:
            pair[0].point += 0.5
            pair[1].point += 0.5


class ReportController:
    def __init__(self):
        self.report_view = ReportView()
        self.players = AddPlayerController().players

    def __call__(self):
        choice = self.report_view.report_choice()
        self.report_view._choices[int(choice)][1]
        return HomeMenuController


class SaveController:
    def __int__(self):
        self.players = AddPlayerController()
        self.tournaments = CreateTournamentController()

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
