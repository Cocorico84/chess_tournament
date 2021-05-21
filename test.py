from tinydb import TinyDB, where, Query
from tinydb.operations import set, add
from models import Player
from utils.utils import flatten_list

db = TinyDB('db.json')

tournaments_table = db.table('tournaments').get(Query().name == 'hello')
players_table = db.table('players')
# player = Player(first_name='coco')
tournament = 'hello'

# q = tournaments_table.update(
#             add("players", [player.first_name]),
#             where('name') == 'pouet'
#         )
# print(q)

# db.table('players').search(Query().first_name.one_of([db.table('tournaments').search(Query().field == 'players')]))


# print(players_table.search(Query().first_name.one_of(tournaments_table['players'])))

# ajout des ids des joueurs au lieu de l'instance
# player_one = db.table('players').get(Query().first_name == 'b')
# player_two = db.table('players').get(Query().first_name == 'gg')
# db.table("tournaments").upsert({"rounds": {1: (player_one.doc_id, player_two.doc_id)}}, Query().name == "hello")

# players_table.update(
#     add('points', 1), Query().first_name == 'b'
# )

# player = Player(first_name='b')
# player = players_table.get(Query().first_name == 'babar')
# db.table('tournaments').update(
#     add('players', [player.doc_id]), Query().name == 'hello'
# )

# first_names = [i['first_name'] for i in db.table('players')]
# print(first_names)
# ids = db.table('tournaments').get(Query().name == 'hello')['players']
#
# print([db.table('players').get(doc_id=number) for number in ids])


# [i for i in db.table('players').all() if i.doc_id in ids]
# print(db.table('players').get(doc_id=ids))
# from models import Tournament, Player
#
# player_table = db.table("players")
# print([Player(**player) for player in player_table.all()])
# tournament_table = db.table("tournaments")
# print([Tournament(**tournament) for tournament in tournament_table.all()])

from models import Database, Tournament
# # print([tournament for tournament in Database().load_tournament_data() if tournament.name == 'hello'][0].__dict__)
# import json
# tournament_table = db.table("tournaments")
# # print([tournament for tournament in tournament_table.all()][0])
# # for key, value in tournament_table.all()[0]:
# #     print(key,value)
# for i in (json.loads(json.dumps(tournament_table.all()))):
#     if i['name'] == 'hello':
#         print(i['rounds'])

# print(db.table("tournaments").get(where('name') == 'hello')['players'])

# print(db.table('players').get(doc_id=1))
# db.table('players').update(add('point', 1), doc_ids=[1])

# print(flatten_list(list(db.table('tournaments').get(where('name') == 'hello')['rounds'][-1].values())))

for i in players_table.all():
    if i['first_name'] == 'b' and i['last_name'] == 'he':
        print(i)