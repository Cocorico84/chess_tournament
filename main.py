from controllers import controller
from views import view
from models import tournament, player
from random import randint

if __name__ == "__main__":
    tournament = tournament.Tournament(name="Test")

    # players = controller.add_player()

    # 8 false players
    players = [player.Player(first_name=str(i), rank=randint(0, 100)) for i in range(8)]

    # 1st Round
    players = controller.order_players_by_rank(players)
    pairs = controller.get_pairs_by_rank(players)
    view.display_pairs(pairs)
    tournament.matches.extend(pairs)
    for pair in pairs:
        view.display_pairs(pair)
        controller.match(pair)
    view.display_players(players)
    print([(player.first_name, player.rank) for player in players])
    tournament.number_of_turns -= 1

    # Next round
    while tournament.number_of_turns > 0:
        players = controller.order_players_by_point(players)
        pairs = controller.get_pairs_by_point(players, tournament.matches)

        for pair in pairs:
            view.display_pairs(pair)
            tournament.matches.append(pair)
            controller.match(pair)
        print(tournament.matches)
        view.display_ranking(players)

        tournament.number_of_turns -= 1
        view.display_left_rounds(tournament.number_of_turns)
