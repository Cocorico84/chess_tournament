def display_players(players: list):
    print([player for player in players])


def display_pairs(pairs: list):
    print([pair for pair in pairs])


def display_points(players: list):
    print("##### Points ##############")
    for player in players:
        print(player.first_name, player.point)


def display_rank(players: list):
    print("########### Ranking ###############")
    for player in players:
        print(player.first_name, player.rank)


def display_match(matches):
    print(matches)


def display_left_rounds(rounds: list):
    print("####### Round ######################")
    print(str(rounds) + " left round")


def display_duration_round(start, end):
    print("################ Duration round ##############")
    print("Round started at", start)
    print("Round finished at", end)
