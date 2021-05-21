from models import Tournament, Player, Round, Database
from utils.menu import Menu
from utils.utils import flatten_list
from view import HomeMenuView, TournamentView, PlayerView, MatchView, QuitView, ReportView, RoundView


class ApplicationController:
    def start(self):
        self.controller = HomeMenuController()
        while self.controller:
            self.controller = self.controller()


class HomeMenuController:
    def __init__(self):
        self.menu = Menu()
        self.view = HomeMenuView(self.menu)

    def __call__(self):
        self.menu.add("auto", "create a tournament", CreateTournamentController())
        self.menu.add("auto", "add a player", AddPlayerController())
        self.menu.add("auto", "write a match result", MatchResultController())
        self.menu.add("auto", "get a report", ReportController())
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
        self.db = Database()
        self.players = self.db.load_player_data()

    def __call__(self):
        player_infos = self.player_view.add_player()
        player_first_name = player_infos[0]
        player_last_name = player_infos[1]

        if (player_first_name, player_last_name) not in [(i.first_name, i.last_name) for i in self.players]:
            Player(first_name=player_first_name, last_name=player_last_name).save_in_db()

        tournament_choice = self.player_view.choose_tournament_to_add_player()
        tournament = Tournament(name=tournament_choice)
        for player in self.players:
            if player.first_name == player_first_name and player.last_name == player_last_name:
                player = player.get_document_from_instance()
                if tournament.len_players < 8:
                    tournament.add_player_in_tournament(player, tournament_choice)

        return HomeMenuController()


class MatchResultController:
    def __init__(self):
        self.round_view = RoundView()
        self.match_view = MatchView()

    def __call__(self):
        tournament_choice = self.round_view.get_tournament_choice()
        self.round = Round(tournament_choice)
        self.players = self.round.players

        if len(self.round.tournament['players']) < 8:
            return AddPlayerController()

        round_is_over = self.round_view.round_over()

        if round_is_over:

            pairs = self.round.sorted_pairs(self.players)
            print(pairs)
            self.round.add_matches_in_tournament(pairs, tournament_choice)
            self.round.save_pairs_in_db(tournament_choice, pairs)
        else:
            pairs = flatten_list(list(self.round.tournament['rounds'][-1].values()))

        self.match_view.display_matches(pairs)

        pair_played_choice = self.match_view.get_match_played()
        pair = pairs[pair_played_choice]

        # TODO supprimer la pair qui a été sortie
        print(pair)
        draw = self.match_view.ask_if_draw()

        if draw == 'N':
            winner = self.match_view.get_the_winner()
            self.round.winner_match(winner)
        else:
            self.round.draw_match(pair)

        return HomeMenuController()


class ReportController:
    def __init__(self):
        self.report_view = ReportView()
        self.db = Database()

    def __call__(self):
        choice = self.report_view.report_choice()
        if choice < 6:
            self.db.get_report(choice)
        else:
            tournament_choice = self.report_view.get_tournament_choice()
            self.db.get_report(choice, tournament_choice)
        return HomeMenuController()


class QuitController:
    def __init__(self):
        self.quit_view = QuitView()

    def __call__(self):
        self.quit_view()
