from controllers import controller
from views import view, report
from models import Tournament, Player, Round
from utils.menu import Menu
from tinydb import TinyDB
from random import randint

a = 'azertyuiop'

db = TinyDB("db.json")


class App:
    def __init__(self):
        self.menu = Menu()

        self.menu.add_choice("create tournament")
        self.menu.add_choice("add players")
        self.menu.add_choice("launch round")
        self.menu.add_choice("write match result")
        self.menu.add_choice("get a report")
        self.menu.add_choice("save in db")
        self.menu.add_choice("quit")

        self.controller = controller.Controller()
        self.view = view.View()

        # self.players = []
        self.players = [Player(first_name=str(i), last_name=a[i], rank=randint(0, 100)) for i in range(8)]
        # self.tournaments = [tournament.Tournament(name=str(i), location=a[i]) for i in range(8)]
        self.tournaments = []

    def start(self):
        while True:
            print(self.menu.choices)
            choice = self.controller.choice()

            if choice == 1:
                tournament_name = input("What name do you want to call it ? ")
                chess_tournament = Tournament(name=tournament_name, location='paris')
                self.tournaments.append(chess_tournament)

            elif choice == 2:
                if len(self.players) < 9:
                    first_name = input("First name of the player: ")
                    last_name = input("Last name of the player: ")
                    rank = int(input("Ranking of the player: "))
                    chess_player = Player(
                        first_name=first_name,
                        last_name=last_name,
                        rank=rank
                    )
                    self.players.append(chess_player)
                    chess_tournament.players.append(chess_player)
                else:
                    self.view.error_players()

            elif choice == 3:
                if len(self.players) == 8:
                    if len(chess_tournament.rounds) < 4:
                        chess_round = Round(name=f"Round {len(chess_tournament.rounds) + 1}")
                        chess_tournament.rounds.append(chess_round)
                    else:
                        self.view.error_round()
                else:
                    self.view.error_players()

            elif choice == 4:
                if len(chess_tournament.rounds) == 1 and chess_tournament.number_of_matches < 4:
                    self.controller.first_round(self.players, chess_tournament)
                elif len(chess_tournament.rounds) > 1 and chess_tournament.number_of_matches % 4 != 0:
                    self.controller.play_a_round(self.players, chess_tournament)

                if chess_tournament.number_of_matches % 4 == 0 and chess_tournament.number_of_matches != 0:
                    chess_round.round_done = True
                    self.view.display_duration_round(chess_round.start_time, chess_round.end_date)

            elif choice == 5:
                print(report.players_ranking_report(self.players))
                print(report.players_from_tournament(db))

            elif choice == 6:
                save = int(input("Save tournament [1], players [2] or both [3] ? "))

                if save == 1:
                    self.controller.save_tournaments(self.tournaments)
                elif save == 2:
                    self.controller.save_players(self.players)
                elif save == 3:
                    self.controller.save_tournaments(self.tournaments)
                    self.controller.save_players(self.players)

            else:
                break
