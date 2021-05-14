from tinydb import TinyDB, where, Query
from tinydb.operations import set, add
from models import Player

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
ids = db.table('tournaments').get(Query().name == 'hello')['players']

print([db.table('players').get(doc_id=number) for number in ids])


# [i for i in db.table('players').all() if i.doc_id in ids]
# print(db.table('players').get(doc_id=ids))
