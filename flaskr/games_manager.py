from flaskr.json_encoder import JSONEncoder
from flaskr.game import Game
from flaskr.player import Player
from flaskr.game_stats import GameStats
from flaskr.shared.question_factory import QuestionFactory

DEFAULT_DELAY = 5
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