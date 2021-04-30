class View:
    def __init__(self):
        pass

    def display_players(self, players: list):
        print([player for player in players])

    def display_pairs(self, pairs: list):
        print([pair for pair in pairs])

    def display_points(self, players: list):
        print("##### Points ##############")
        for player in players:
            print(player.first_name, player.point)

    def display_rank(self, players: list):
        print("########### Ranking ###############")
        for player in players:
            print(player.first_name, player.rank)

    def display_match(self, matches):
        print(matches)

    def display_left_rounds(self, rounds: list):
        print("####### Round ######################")
        print(str(rounds) + " left round")

    def display_duration_round(self, start, end):
        print("################ Duration round ##############")
        print("Round started at", start)
        print("Round finished at", end)

    def error_players(self):
        print("Problem with number of required players")

    def error_round(self):
        print("All rounds have been played or all matches haven't been played in the current round")