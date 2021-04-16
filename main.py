from controllers import controller
from views import view
from models import tournament

if __name__ == "__main__":
    tournament = tournament.Tournament(name="Test")

    players = controller.add_player()

    # 1st Round
    players = controller.order_players_by_rank(players)
    print(players)
    pairs = controller.get_pairs_from_rank(players)
    print(pairs)
    tournament.number_of_turns -= 1
    # print(tournament.number_of_turns)

    results = []
    for pair in pairs:
        print(pair)
        controller.match(pair)
    for player in players:
        print(player.first_name, player.point)

    while tournament.number_of_turns > 0:
        # enlever le dernier du classement
        # recommencer le pairing

        tournament.number_of_turns -= 1
