import json
from uuid import uuid4
from flaskr.shared.dynamo_db import *
from flaskr.shared.question_factory import (MAX_ROUND)
from flaskr.json_encoder import JSONEncoder
from flaskr.game import Game
from flaskr.player import Player
from flaskr.game_stats import GameStats
from flaskr.shared.question_factory import QuestionFactory

sqs_client = boto3.client('sqs')
sqs_resource = boto3.resource('sqs')

DEFAULT_DELAY = 5


class AWSGamesManager:
    """ Game manager class for lambda functions and backend server to interface with the DynamoDB """

    def __init__(self):
        self.question_factory = QuestionFactory()

        try:
            self.queue = sqs_resource.create_queue(
                QueueName='GameTasks'
            )
        except sqs_client.exceptions.QueueNameExists:
            self.queue = sqs_resource.get_queue_by_name(QueueName='GameTasks')
        except sqs_client.exceptions.QueueDeletedRecently:
            raise

    # GAME MANAGEMENT

    def game_exists(self, game_id) -> bool:
        """ Checks if game_id exists in database """
        return game_id in db_get_game_ids()

    def get_all_games(self) -> dict:
        """ Returns dict containing all games in the database """
        return db_get_all_games()

    def get_game(self, game_id) -> dict:
        """ Returns corresponding game for given game_id """
        return db_get_game(game_id)

    def new_game(self, password, round=0) -> dict:
        """ Creates a new game in the database and returns newly created <game_id>"""
        assert password.strip() != ""

        gid, modification_hash = db_add_new_game(password, round=0)

        # Start game monitor thread
        self.queue.send_message(
            MessageBody=str(gid),
            DelaySeconds=0,
            MessageAttributes={
                'MessageType': {
                    'StringValue': 'Monitor',
                    'DataType': 'String'
                },
                'ModificationHash': {
                    'StringValue': modification_hash,
                    'DataType': 'String'
                }
            }
        )

        return gid

    def game_ended(self, game_id) -> bool:
        """ returns True if game has ended, False if not """
        return db_game_ended(game_id)

    def game_has_password(self, game_id, password) -> bool:
        """ Checks that game password equals given password """
        return db_get_game_password(game_id) == password

    def game_in_last_round(self, game_id) -> bool:
        """ Check if game is in its final round """
        return db_get_round(game_id) == MAX_ROUND

    def advance_game_round(self, game_id):
        """ Advances game round """
        db_advance_round(game_id)
        db_reset_round_indices(game_id)

    def pause_game(self, game_id):
        """ Pause a game """
        db_set_paused(game_id, True)

    def unpause_game(self, game_id):
        """ Unpause a game """
        db_set_paused(game_id, False)

    def end_game(self, game_id):
        """ Ends a game """
        db_end_game(game_id)

    def set_auto_mode(self, game_id):
        """ Turns on auto advance round """
        db_set_auto_mode(game_id, True)

    def clear_auto_mode(self, game_id):
        """ Turns off auto advance round """
        db_set_auto_mode(game_id, False)

    # PLAYER MANAGEMENT

    def get_game_players(self, game_id, *player_id) -> dict:
        """ If player_id(s) given, returns Player objects for only those players, 
            else returns all Player objects """

        if player_id:
            return {pid: db_get_player(game_id, pid) for pid in list(player_id)}
        else:
            return db_get_all_players(game_id)

    def player_exists(self, game_id, player_id) -> bool:
        """ Checks if player_id exists in the given game """
        return player_id in db_get_player_ids(game_id)

    def get_game_running_totals(self, game_id) -> list:
        """ Gets list of objects in the form {"time": timestamp, "pid": score} """

        return db_get_scores(game_id)

    def get_score_for_player(self, game_id, player_id) -> int:
        # This function is unused as far as I can see
        """ Returns a player's score """

        return db_get_player_score(game_id, player_id)

    def add_player_to_game(self, game_id, name, api) -> dict:
        """ Adds a player to a game and returns newly added player """
        new_player, modification_hash = db_add_player(game_id, name, api)
        curr_round = db_get_round(game_id)
        next_question = self.question_factory.next_question(curr_round)

        message = {
            "game_id": game_id,
            "player_id": new_player['id'],
            "question_text": next_question.as_text(),
            "question_answer": next_question.correct_answer(),
            "prev_delay": DEFAULT_DELAY,
            "question_points": next_question.points,
            "question_difficulty": curr_round
        }

        # Start administering questions
        self.queue.send_message(
            MessageBody=json.dumps(message),
            DelaySeconds=0,
            MessageAttributes={
                'MessageType': {
                    'StringValue': 'AdministerQuestion',
                    'DataType': 'String'
                },
                'ModificationHash': {
                    'StringValue': modification_hash,
                    'DataType': 'String'
                },
            }
        )
        print(f"Server has sent player message {message}")

        return new_player

    def get_players_to_assist(self, game_id) -> dict:
        """ Returns names of players to assist in the form { "needs_assistance": [], "being_assisted": [] } """

        return db_get_players_to_assist(game_id)

    def assist_player(self, game_id, player_name):
        """ Updates a player's state from 'needing assistance' to 'being assisted' """
        return db_assist_player(game_id, player_name)

    def update_player(self, game_id, player_id, name=None, api=None):
        """ Updates name and api of player """
        db_update_player(game_id, player_id, name, api)

    def get_player_events(self, game_id, player_id) -> list:
        """ Returns list of event objects for a player """

        return db_get_events(game_id, player_id)

    def remove_game_players(self, game_id, *player_id):
        """ If player_id(s) provded, deletes corresponding players, else deletes all players for a given game """

        if player_id:
            for pid in list(player_id):
                db_delete_player(game_id, pid)
        else:
            db_delete_all_players(game_id)

    # Methods used after game is ended
    def delete_games(self, *game_id):
        """ If game_id(s) provided, deletes those games, else deletes all games """

        gids = game_id if game_id else db_get_game_ids()

        for gid in list(gids):
            player_data = db_get_all_players(gid)
            scoreboard_data = db_get_scoreboard(gid)
            analysis_event_data = db_get_analysis_events(gid)

            db_end_game(gid)
            # Need to make sure to stop/kill all threads
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

    def review_exists(self, game_id):
        return db_review_exists(game_id)
