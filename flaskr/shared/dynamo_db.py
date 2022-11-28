import boto3
from uuid import uuid4

db = boto3.resource('dynamodb').Table('Games')

def db_get_all_games():
    return {} # NOT IMPLEMENTED.

def db_get_game(game_id):
    return db.get_item(Key={'game_id': game_id})

def db_add_new_game(password):
    id = uuid4().hex[:8]
    return

def db_get_player_score(game_id, player_id):
    game = db_get_game(game_id)

    return

def db_get_game_ids():
    """ Returns list of game ids """
    return

def db_get_player_ids(game_id):
    """ Returns list of player ids in a game """
    return