def order_players_by_key(my_list: list, my_key) -> list:
    return sorted(my_list, key=lambda x: x[my_key], reverse=True)


def flatten_list(a):
    return sum(a, [])
