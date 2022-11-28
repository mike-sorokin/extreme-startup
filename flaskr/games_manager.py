from flaskr.json_encoder import JSONEncoder
from flaskr.game import Game
from flaskr.player import Player
from flaskr.game_stats import GameStats


# Manages all active game instances -- instructing what games should modify when live and also in charge
# of uploading relevant game information to the DB upon game termination 
class GamesManager:

    def __init__(self, db_client):
        self.games = {}
        self.db_client = db_client

    def get_all_games(self):
        return self.games

    def get_game(self, game_id):
        if game_id not in self.games:
            return None
        return self.games[game_id]

    def new_game(self, password):
        assert password != ""

        new_game = Game(password)
        gid = new_game.id
        self.games[gid] = new_game
        new_game.spawn_game_monitor()

        return new_game

    def game_exists(self, game_id):
        return game_id in self.games

    def player_exists(self, game_id, player_id):
        return player_id in self.games[game_id].players

    def game_has_password(self, game_id, password):
        return self.games[game_id].compare_password(password)

    def game_in_last_round(self, game_id):
        return self.games[game_id].is_last_round()

    def pause_game(self, game_id):
        self.games[game_id].pause()

    def unpause_game(self, game_id):
        self.games[game_id].spawn_game_monitor()
        self.games[game_id].unpause()

    def end_game(self, game_id):
        self.games[game_id].end()

    def advance_game_round(self, game_id):
        self.games[game_id].advance_round()

    def set_auto_mode(self, game_id):
        self.games[game_id].auto_mode = True

    def clear_auto_mode(self, game_id):
        self.games[game_id].auto_mode = False

    def get_game_running_totals(self, game_id):
        return self.games[game_id].scoreboard.running_totals

    def get_game_players(self, game_id, *player_id):
        return self.games[game_id].get_players(*player_id)

    def get_score_for_player(self, game_id, player_id):
        return self.games[game_id].scoreboard.scores[player_id]

    def remove_game_players(self, game_id, *player_id):
        self.games[game_id].remove_players(*player_id)

    def add_player_to_game(self, game_id, name, api):
        player = Player(game_id, name, api)
        return self.games[game_id].add_player(player)

    def get_players_to_assist(self, game_id):
        return self.games[game_id].players_to_assist

    def update_player(self, game_id, player_id, name=None, api=None):
        self.games[game_id].update_player(player_id, name, api)

    def get_player_events(self, game_id, player_id):
        return self.games[game_id].get_events(player_id)

    def assist_player(self, game_id, player_name):
        self.games[game_id].assist_player(player_name)

    def delete_games(self, *game_id):
        # Delete all game in game_id; if game_id is not provided, delete all games
        gids = game_id if game_id else self.games.keys()

        for gid in list(gids):
            # Copy player/scoreboard data for game review.
            player_data = self.games[gid].get_players()
            scoreboard_data = self.games[gid].scoreboard
            analysis_event_data = self.games[gid].analysis_events

            self.end_game(gid)  # ensures monitor threads are killed
            self.remove_game_players(gid)  # kills administering question threads
            self.unpause_game(gid)  # removes dangling administering question threads
            del self.games[gid]

            if len(player_data) > 0:
                self.analyse_game(gid, player_data, scoreboard_data, analysis_event_data)

    def analyse_game(self, game_id, player_data, scoreboard, analysis_events):
        """
        Args:
        game_id :: uuid4() [8 chars]
        player_data :: { player_id -> Player }
        scoreboard :: Scoreboard
        """ 
        encoded_players, finalboard, stats = GameStats(player_data, scoreboard).generate_game_stats()
        
        finalgraph = scoreboard.running_totals
        finalboard.sort(key=lambda x: -x["score"])

        analysis = [JSONEncoder().default(event) for event in analysis_events]

        # Upload game data + review/analysis
        self.upload_data(
            game_id,
            encoded_players,
            finalboard=finalboard,
            finalgraph=finalgraph,
            finalstats=stats,
            analysis=analysis,
        )

    def upload_data(self, game_id, players_data, **reviews_items):
        self.db_client.xs[f"{game_id}_players"].insert_many(players_data)
        self.db_client.xs[f"{game_id}_review"].insert_many([{"item": k, "stats": v} for k, v in reviews_items.items()])

from uuid import uuid4
from flaskr.shared.dynamo_db import *
from flaskr.question_factory import (MAX_ROUND)

class AWSGamesManager:
    """ Game manager class for lambda functions and backend server to interface with the DynamoDB """

    def __init__(self, db_client):
        self.db_client = db_client

    def get_all_games(self):
        """ Returns list of all game objects in the database """

        return db_get_all_games()

    def get_game(self, game_id):
        """ Returns corresponding game object for given game_id """

        return db_get_game(game_id)

    def new_game(self, password):
        """ Creates a new game in the database """

        assert password.strip() != ""

        # new_game = {
        #     "id": uuid4().hex[:8],
        #     "admin_password": password,
        #     "round": 0,
        #     "players": [],
        #     "paused": False,
        #     "auto_mode": False
        # }
        return db_add_new_game(password)

        # Still need game monitors but not sure how this will work
        # new_game.spawn_game_monitor()

    def game_exists(self, game_id) -> bool:
        """ Checks if game_id exists in database """

        return game_id in db_get_game_ids()

    def player_exists(self, game_id, player_id) -> bool:
        """ Checks if player_id exists in the given game """

        return player_id in db_get_player_ids(game_id)

    def game_has_password(self, game_id, password):
        """ Checks that game password equals given password """
        return db_get_game_password(game_id) == password

    def game_in_last_round(self, game_id):
        """ Check if game is in its final round """
        return db_get_round(game_id) == MAX_ROUND

    def pause_game(self, game_id):
        """ Pause a game """
        # self.games[game_id].pause()
        db_set_paused(game_id, True)

    def unpause_game(self, game_id):
        """ Unpause a game """
        # self.games[game_id].spawn_game_monitor()
        # self.games[game_id].unpause()
        db_set_paused(game_id, False)

    def end_game(self, game_id):
        """ Ends a game """
        db_end_game(game_id)

    def advance_game_round(self, game_id):
        """ Advances game round """
        # self.games[game_id].advance_round()
        db_advance_round(game_id)
        # what is round index and first round event?

    def set_auto_mode(self, game_id):
        """ Turns on auto advance round """
        # self.games[game_id].auto_mode = True
        db_set_auto_mode(game_id, True)

    def clear_auto_mode(self, game_id):
        """ Turns off auto advance round """
        # self.games[game_id].auto_mode = False
        db_set_auto_mode(game_id, False)

    def get_game_running_totals(self, game_id):
        """ Gets list of objects in the form {"time": timestamp, "pid": score} """
        # return self.games[game_id].scoreboard.running_totals
        return db_get_scores(game_id)

    def get_game_players(self, game_id, *player_id):
        """ If player_id given, returns individual player object, else returns """
        # return self.games[game_id].get_players(*player_id)
        players = db_get_all_players(game_id)
        if player_id:
            return players[player_id]
        
        return players

    def get_score_for_player(self, game_id, player_id):
        return self.games[game_id].scoreboard.scores[player_id]

    def remove_game_players(self, game_id, *player_id):
        self.games[game_id].remove_players(*player_id)

    def add_player_to_game(self, game_id, name, api):
        player = Player(game_id, name, api)
        return self.games[game_id].add_player(player)

    def get_players_to_assist(self, game_id):
        return self.games[game_id].players_to_assist

    def update_player(self, game_id, player_id, name=None, api=None):
        self.games[game_id].update_player(player_id, name, api)

    def get_player_events(self, game_id, player_id):
        return self.games[game_id].get_events(player_id)

    def assist_player(self, game_id, player_name):
        self.games[game_id].assist_player(player_name)

    def delete_games(self, *game_id):
        # Delete all game in game_id; if game_id is not provided, delete all games
        gids = game_id if game_id else self.games.keys()

        for gid in list(gids):
            # Copy player/scoreboard data for game review.
            player_data = self.games[gid].get_players()
            scoreboard_data = self.games[gid].scoreboard
            analysis_event_data = self.games[gid].analysis_events

            self.end_game(gid)  # ensures monitor threads are killed
            self.remove_game_players(gid)  # kills administering question threads
            self.unpause_game(gid)  # removes dangling administering question threads
            del self.games[gid]

            if len(player_data) > 0:
                self.analyse_game(gid, player_data, scoreboard_data, analysis_event_data)

    def analyse_game(self, game_id, player_data, scoreboard, analysis_events):
        """
        Args:
        game_id :: uuid4() [8 chars]
        player_data :: { player_id -> Player }
        scoreboard :: Scoreboard
        """ 
        encoded_players, finalboard, stats = GameStats(player_data, scoreboard).generate_game_stats()
        
        finalgraph = scoreboard.running_totals
        finalboard.sort(key=lambda x: -x["score"])

        analysis = [JSONEncoder().default(event) for event in analysis_events]

        # Upload game data + review/analysis
        self.upload_data(
            game_id,
            encoded_players,
            finalboard=finalboard,
            finalgraph=finalgraph,
            finalstats=stats,
            analysis=analysis,
        )

    def upload_data(self, game_id, players_data, **reviews_items):
        self.db_client.xs[f"{game_id}_players"].insert_many(players_data)
        self.db_client.xs[f"{game_id}_review"].insert_many([{"item": k, "stats": v} for k, v in reviews_items.items()])