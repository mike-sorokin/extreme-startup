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

def db_get_round(game_id):
    """ Returns game round """    
    return

def db_get_game_password(game_id):
    """ Returns game password """    
    return

def db_set_paused(game_id, value: bool):
    """ Sets paused to given value (true/false) """ 
    # Need to make sure lambda functions are paused if game is paused
    return

def db_end_game(game_id):
    """ Sets ended to true """ 
    return

def db_advance_round(game_id):
    """ Increments round """ 
    return

def db_set_auto_mode(game_id, value: bool):
    """ Sets auto to given value (true/false) """ 
    return

def db_get_scores(game_id):
    """ Returns game scores as a list of objects in the form {"time": timestamp, "pid": score} """ 
    return

def db_get_all_players(game_id):
    """ Returns players as a dict in the form {player_id: Player, player_id: Player, ...} """ 
    return