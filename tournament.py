from random import randrange


class Tournament:
    def __init__(self, name, location, date, rounds, players, time_control, description, number_of_turns=4):
        self.name = name
        self.location = location
        self.date = date
        self.number_of_turns = number_of_turns
        self.rounds = rounds
        self.players = players
        self.time_control = time_control
        self.description = description

    def order_player(self, players):
        return sorted(players, key=players.rank)

    def get_pairs(self, players):
        pairs_list = []
        while len(players) >= 0:
            player_one = randrange(0, len(players))
            players.pop(player_one)
            player_two = randrange(0, len(players))
            players.pop(player_two)
            pairs_list.append((player_one, player_two))

        return pairs_list

    def match(self, player_one, player_two):
        if player_one:
            player_one[1] += 1
        elif player_two:
            player_two += 1
        else:
            player_one += 0.5
            player_two += 0.5

    def write_results(self, winner, loser):
        pass
        # player_one[]
        # player_two[]

    @property
    def turn(self):
        return self.rounds + 1
