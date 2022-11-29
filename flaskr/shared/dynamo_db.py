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

def db_is_game_paused(game_id):
    """ Returns true if game is paused false if not """    
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

def db_get_player(game_id, player_id):
    """ Returns player object """ 
    return

def db_delete_player(game_id, player_id):
    """ Deletes player """ 
    return

def db_delete_all_players(game_id):
    """ Deletes all players """ 
    return

def db_add_player(game_id, name, api):
    """ Add player and return created player object """ 
    return

def db_get_players_to_assist(game_id):
    """ Returns names of players to assist in the form { "needs_assistance": [], "being_assisted": [] } """ 
    return

def db_assist_player(game_id, player_name):
    """ Updates a player's state from 'needing assistance' to 'being assisted' """ 
    return

def db_update_player(game_id, player_id, name, api):
    """ Updates name and api of player """ 
    # I don't think this is ever used currently
    return

def db_get_events(game_id, player_id):
    """ Returns list of event objects for a player """ 
    return

def db_get_scoreboard(game_id):
    """ Returns Scoreboard object for a game (or at least a mock version) """ 
    return

def db_get_analysis_events(game_id):
    """ Returns analysis events for a game (not sure what this means) """ 
    return