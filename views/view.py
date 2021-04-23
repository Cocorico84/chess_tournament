from controllers import controller


def display_players(players: list):
    print([player for player in players])


def display_pairs(pairs: list):
    print([pair for pair in pairs])


def display_ranking(players: list):
    for player in players:
        print(player.first_name, player.point)


def display_left_rounds(rounds: list):
    print(str(rounds) + " left round")
