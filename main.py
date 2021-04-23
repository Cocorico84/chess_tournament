from controllers import controller
from views import view, report
from models import tournament, player, round
from random import randint
from tinydb import TinyDB

a = 'azertyuiop'
db = TinyDB("db.json")

if __name__ == "__main__":
    tournament = tournament.Tournament(name="Test")

    # players = controller.add_player()

    # 8 false players
    players = [player.Player(first_name=str(i), last_name=a[i], rank=randint(0, 100)) for i in range(8)]

    # save in db
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
        players_table = db.table('players')
        players_table.truncate()
        players_table.insert_multiple(serialized_players)

    # print(report.players_ranking_report(players))

    # 1st Round
    round = round.Round(name="1")
    controller.first_round(players, tournament)
    round.round_done = True
    view.display_duration_round(round.start_time, round.end_date)

    # Next round
    controller.play_a_round(players, tournament)
    controller.play_a_round(players, tournament)
    controller.play_a_round(players, tournament)
    print(len(tournament.matches))
