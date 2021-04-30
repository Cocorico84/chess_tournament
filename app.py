from controllers import controller
from views import view, report
from models import tournament, player, round, menu
from tinydb import TinyDB
from random import randint

a = 'azertyuiop'

db = TinyDB("db.json")

if __name__ == "__main__":
    menu = menu.Menu()
    menu.add_choice("create tournament")
    menu.add_choice("add players")
    menu.add_choice("launch round")
    menu.add_choice("write match result")
    menu.add_choice("get a report")
    menu.add_choice("save in db")
    menu.add_choice("quit")

    controller = controller.Controller()
    view = view.View()

    while True:
        print(menu.choices)
        choice = controller.choice()

        # players = []
        players = [player.Player(first_name=str(i), last_name=a[i], rank=randint(0, 100)) for i in range(8)]
        tournaments = [tournament.Tournament(name=str(i), location=a[i]) for i in range(8)]
        # tournaments = []

        if choice == 1:
            tournament_name = input("What name do you want to call it ? ")
            # chess_tournament = tournament.Tournament(name=tournament_name)
            chess_tournament = tournament.Tournament(name=tournament_name, location='paris')
            tournaments.append(chess_tournament)

        elif choice == 2:
            if len(players) < 9:
                first_name = input("First name of the player: ")
                last_name = input("Last name of the player: ")
                rank = int(input("Ranking of the player"))
                chess_player = player.Player(
                    first_name=first_name,
                    last_name=last_name,
                    rank=rank
                )
                players.append(chess_player)
                chess_tournament.players.append(chess_player)
            else:
                view.error_players()

        elif choice == 3:
            if len(players) == 8:
                if len(chess_tournament.rounds) < 4:
                    chess_round = round.Round(name=f"Round {len(chess_tournament.rounds) + 1}")
                    chess_tournament.rounds.append(chess_round)
                else:
                    view.error_round()
            else:
                view.error_players()

        elif choice == 4:
            if len(chess_tournament.rounds) == 1 and chess_tournament.number_of_matches != 4:
                controller.first_round(players, chess_tournament)
            elif len(chess_tournament.rounds) > 1 and chess_tournament.number_of_matches % 4 != 0:
                controller.play_a_round(players, chess_tournament)

            if chess_tournament.number_of_matches % 4 == 0 and chess_tournament.number_of_matches != 0:
                chess_round.round_done = True
                view.display_duration_round(chess_round.start_time, chess_round.end_date)

        elif choice == 5:
            print(report.players_ranking_report(players))
            print(report.players_from_tournament(db))

        elif choice == 6:
            save = int(input("Save tournament [1], players [2] or both [3] ? "))

            if save == 1:
                controller.save_tournaments(tournaments)
            elif save == 2:
                controller.save_players(players)
            elif save == 3:
                controller.save_tournaments(tournaments)
                controller.save_players(players)

        else:
            break
