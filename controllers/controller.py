from random import shuffle
from views import view
from models import match, player, round, tournament


def add_player():
    players = []
    for i in range(8):
        name_player = input("Enter player's name: ")
        players.append(player.Player(first_name=name_player))
    return players


def order_players_by_rank(players: list) -> list:
    return sorted(players, key=lambda x: x.rank)


def get_pairs_from_rank(players: list) -> list:
    pairs_list = []
    list_one = players[:4]
    list_two = players[4:]
    for i, j in zip(list_one, list_two):
        pairs_list.append([i, j])

    return pairs_list


def get_pairs(players: list) -> list:
    pairs_list = []
    shuffle(players)
    for i in range(0, len(players), 2):
        pairs_list.append(players[i:i + 2])

    return pairs_list


def match(pair):
    winner = input("Who's the winner ? ")
    if winner == pair[0].first_name:
        pair[0].point += 1
    elif winner == pair[1].first_name:
        pair[1].point += 1
    else:
        pair[0].point += 0.5
        pair[1].point += 0.5
