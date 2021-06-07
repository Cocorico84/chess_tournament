from typing import Optional

from models import Tournament, Player, Database
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
        self.menu.add("auto", "write a match result", MatchResultController())
        self.menu.add("auto", "change player rank", ChangeRankController())
        self.menu.add("auto", "get a report", ReportController())
        self.menu.add("q", "quit", QuitController())

        user_choice = self.view.get_user_choice()

        return user_choice.handler


class CreateTournamentController:
    """
    This controller creates a tournament and allows to add 8 players. The tournament and the 8 players are savend in
    the database in their own table.
    """

    def __init__(self):
        self.tournament_view = TournamentView()
        self.player_view = PlayerView()
        self.db = Database()
        self.players = self.db.load_player_data()

    def __call__(self):
        if len(self.db.all_tournaments_in_progress()) > 0:
            self.tournament_view.display_error_tournament_active()
        else:
            tournament_infos = self.tournament_view.get_info()
            tournament = Tournament(
                name=tournament_infos[0],
                location=tournament_infos[1],
                number_of_turns=tournament_infos[2],
                description=tournament_infos[3],
                time_control=tournament_infos[4]
            )
            tournament.save_in_db()

            self.add_a_player(tournament=tournament)

        return HomeMenuController()

    def add_a_player(self, tournament: Tournament):
        """
        Create a player instance and save data in the table "players" from the database
        """
        player_infos = self.player_view.add_player()
        player_first_name = player_infos[0]
        player_last_name = player_infos[1]
        player_birth = player_infos[2]
        player_gender = player_infos[3]

        if (player_first_name, player_last_name) not in [(i.first_name, i.last_name) for i in self.players]:
            Player(first_name=player_first_name,
                   last_name=player_last_name,
                   birth=player_birth,
                   gender=player_gender
                   ).save_in_db()

        for player in self.players:
            if player.first_name == player_first_name and player.last_name == player_last_name:
                player = player.get_document_from_instance()
                if tournament.number_of_players < 8:
                    tournament.add_player_in_tournament(player)


class MatchResultController:
    """
    This controller allows to write results and save in the database.
    """
    def __init__(self):
        self.round_view = RoundView()
        self.match_view = MatchView()

    def __call__(self):
        if len(Database().all_tournaments_in_progress()) == 0:
            self.round_view.error_no_active_tournament()
            return HomeMenuController()
        else:
            self.tournament = Database().all_tournaments_in_progress()[0]

        self.match_view.display_active_tournament(self.tournament)
        self.players = self.tournament.get_players_from_tournament()

        if len(self.tournament.rounds) != 0:
            pairs = flatten_list(list(self.tournament.rounds[-1].values()))
        else:
            pairs = []

        left_matches = len(self.tournament.matches_not_played(pairs))
        self.round_view.display_if_round_over(left_matches)
        if left_matches > 0:
            if left_matches == 1:
                self.tournament.update_end_round()
                if self.tournament.left_round == 0:
                    self.tournament.is_active = False
                    self.tournament.save_in_db()
            pairs = self.tournament.matches_not_played(pairs)
        else:
            pairs = self.tournament.sorted_pairs(self.players)
            self.tournament.create_round()

            self.tournament.save_pairs_in_db(pairs)

        pairs = self.tournament.matches_not_played(pairs)
        self.match_view.display_matches(self.tournament.get_name_from_ids(pairs))

        pair_played_choice = self.match_view.get_match_played()
        pair = pairs[pair_played_choice]
        self.tournament.add_matches_in_tournament(pair)

        draw = self.match_view.ask_if_draw()

        if draw == 'N':
            winner = self.match_view.get_the_winner()
            self.tournament.winner_match(winner)
            self.tournament.create_match(pair, winner)
        else:
            self.tournament.draw_match(pair)
            self.tournament.create_match(pair, "D")

        return HomeMenuController()


class ChangeRankController:
    """
    This controller changes the rank of the player form his first name and his last name
    """
    def __init__(self):
        self.player = PlayerView()
        self.db = Database()

    def __call__(self):
        player_info = self.player.get_first_name_last_name()
        player = Player(first_name=player_info[0], last_name=player_info[1])
        player.update_rank(player_info[2])
        return HomeMenuController()


class ReportController:
    """
    Check the right choice to get the report
    """
    def __init__(self):
        self.report_view = ReportView()
        self.db = Database()

    def __call__(self):
        choice = self.report_view.report_choice()
        if choice in [1, 2, 5]:
            report = self.get_report(choice)
        else:
            self.report_view.display_tournament_names(self.db.load_tournament_data())
            tournament_choice = self.report_view.get_tournament_choice()
            report = self.get_report(choice, tournament_choice)
        if choice in [1, 2, 3, 4]:
            self.report_view.display_players_report(report)
        elif choice == 5:
            self.report_view.display_tournament(report)
        elif choice == 6:
            self.report_view.display_rounds(report)
        elif choice == 7:
            self.report_view.display_matches(report)
        return HomeMenuController()

    def get_report(self, choice_number: int, tournament_name: Optional[str] = None):
        valid_commands = {
            1: "players_alpha_report",
            2: "players_ranking_report",
            3: "players_alpha_report",
            4: "players_ranking_report",
            5: "get_all_tournaments",
            6: "get_rounds_of_tournament",
            7: "get_matches_of_tournament"
        }
        if tournament_name is None:
            return getattr(self.db, valid_commands[choice_number])()
        else:
            return getattr(self.db, valid_commands[choice_number])(tournament_name)


class QuitController:
    def __init__(self):
        self.quit_view = QuitView()

    def __call__(self):
        self.quit_view()
