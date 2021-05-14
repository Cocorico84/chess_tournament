from random import shuffle
from tinydb import TinyDB, Query, where
from tinydb.operations import add, set
from models import Tournament, Player, Round, Database
from utils.menu import Menu
from view import HomeMenuView, TournamentView, PlayerView, MatchView, QuitView, ReportView, RoundView

db = TinyDB("db.json")


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
        self.tournaments = db.table('tournaments')
        self.players = db.table('players')

    def __call__(self):
        # TODO check si le tournoi existe quand on ajoute un joueur
        player = self.player_view.add_player()
        if player not in [i['first_name'] for i in self.players]:
            Player(first_name=player).save_in_db()
        tournament_choice = self.player_view.add_player_into_tournament()
        tournament = self.tournaments.get(where('name') == tournament_choice)
        player = self.players.get(where('first_name') == player)
        self.tournaments.update(
            add("players", [player.doc_id]),
            where('name') == tournament['name']
        )
        return HomeMenuController()


class LaunchRoundController:
    def __init__(self):
        self.match = MatchResultController()
        self.round_view = RoundView()
        self.tournaments = db.table("tournaments")

    def __call__(self):
        # TODO vérifier qu'il y 8 joueurs dans le tournoi sélectionné
        choice = self.round_view.get_tournament_choice()
        tournament = self.tournaments.get(where("name") == choice)
        self.tournaments.update(
            add("rounds", [{len(tournament["rounds"]) + 1: []}]),
            where("name") == choice
        )
        self.round_view()
        return HomeMenuController()


class MatchResultController:
    # TODO réussir à mettre les matches dans les rounds sous forme de liste et rentrer les rounds sous forme de dico

    # TODO prendre tous les joueurs puis les filtrer en fonction du tournoi

    def __init__(self):
        # self.tournament_choice = RoundView().get_tournament_choice()
        self.match_view = MatchView()
        self.tournaments = db.table("tournaments")
        self.tournament = db.table('tournaments').get(Query().name == 'hello')
        self.rounds = self.tournament['rounds']

        # self.players = [Player(**i) for i in db.table('players').search(
        #     Query().first_name.one_of(db.table('tournaments').get(Query().name == 'hello')['players'])
        # )]
        # self.players = db.table('players').search(
        #     Query().first_name.one_of(db.table('tournaments').get(Query().name == 'hello')['players'])
        # )
        self.player_ids = self.tournament['players']
        self.players = [i for i in db.table('players').all() if i.doc_id in self.player_ids]


    def __call__(self):
        players = self.order_players_by_rank(self.players) if '1' in self.rounds[0].keys() else self.order_players_by_point(
            self.players)
        pairs = self.get_pairs_by_rank(self.player_ids) if '1' in self.rounds[0].keys() else self.get_pairs_by_point(players, self.get_pairs(self.player_ids))

        self.tournaments.upsert(
            {"rounds":  [{"1": pairs}]},
            Query().name == "hello"
        )

        self.match_view._display_matches(pairs)

        pair_played_choice = self.match_view.get_match_played()
        pair = pairs[pair_played_choice]
        print(pair)
        draw = self.match_view._ask_if_draw()
        if draw == 'N':
            winner = self.match_view.get_the_winner()
            winner_name = db.table('players').get(doc_id=winner)['first_name']
            print(winner_name)
            self.winner_match(winner_name)
        else:
            self.draw_match(pair)

        return HomeMenuController()

    def winner_match(self, winner: str):
        db.table('players').update(
            add('point', 1),
            where("first_name") == winner
        )

    def draw_match(self, pair):
        db.table('players').update(
            add('point', 0.5),
            Query().first_name == pair[0]
        )
        db.table('players').update(
            add('point', 0.5),
            Query().first_name == pair[1]
        )

    def order_players_by_rank(self, players: list) -> list:
        return sorted(players, key=lambda x: x['rank'], reverse=True)

    def order_players_by_point(self, players: list) -> list:
        return sorted(players, key=lambda x: x['point'], reverse=True)

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

    def __call__(self):
        choice = self.report_view.report_choice()
        self.report_view._choices[int(choice)][1](db)
        return HomeMenuController()


class SaveController:
    # def __int__(self):
    # self.players = db.load_player_data()
    # self.tournaments = db.load_tournament_data()

    def __call__(self):
        # for player in self.players:
        #     player.save_in_db()
        #
        # for tournament in self.tournaments:
        #     tournament.save_in_db()
        return HomeMenuController()


class QuitController:
    def __init__(self):
        self.quit_view = QuitView()

    def __call__(self):
        self.quit_view()
