from tinydb import TinyDB, where, Query
from tinydb.operations import set, add
from models import Player
from utils.utils import flatten_list

db = TinyDB('db.json')

players_table = db.table('players')
# player = Player(first_name='coco')

# pair = [1,10]
# tournament_players = db.table('tournaments').get(Query().name == 'papa')['players']
# for i in players_table:
#     if i.doc_id in pair:
#         print({i.doc_id: (i['first_name'], i['last_name'])})
#
print(sum([[1, 10]], []))
