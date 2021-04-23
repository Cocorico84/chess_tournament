import pandas as pd


def players_alpha_report(players):
    report = []
    for player in sorted(players, key=lambda x: x.last_name):
        report.append({'first_name': player.first_name, 'last_name': player.last_name})

    print(pd.DataFrame(report))


def players_ranking_report(players):
    report = []
    for player in sorted(players, key=lambda x: x.rank, reverse=True):
        report.append({'first_name': player.first_name, 'last_name': player.last_name, 'ranking': player.rank})

    print(pd.DataFrame(report))
