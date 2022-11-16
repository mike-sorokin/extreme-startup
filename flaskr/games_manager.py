from flaskr.json_encoder import JSONEncoder
from flaskr.game import Game
from flaskr.player import Player


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

    def delete_games(self, *game_id):
        # Delete all game in game_id; if game_id is not provided, delete all games
        gids = game_id if game_id else self.games.keys()

        for gid in list(gids):
            # Copy player/scoreboard data for game review.
            player_data = self.games[gid].get_players()
            scoreboard_data = self.games[gid].scoreboard

            self.end_game(gid)  # ensures monitor threads are killed
            self.remove_game_players(gid)  # kills administering question threads
            self.unpause_game(gid)  # removes dangling administering question threads
            del self.games[gid]

            if len(player_data) > 0:
                self.analyse_game(gid, player_data, scoreboard_data)

    def analyse_game(self, game_id, player_data, scoreboard):
        """
        Args:
        game_id :: uuid4() [8 chars]
        player_data :: { player_id -> Player }
        scoreboard :: Scoreboard
        """

        encoded_players = []
        finalboard = {}
        finalgraph = scoreboard.running_totals
        stats = {}
        analysis = []

        num_players = len(player_data) 

        total_requests = 0
        total_player_avg_streak = 0.0

        total_on_fire_duration = 0
        total_num_of_on_fires = 0

        longest_streak_length = 0
        longest_on_fire_duration = 0 
        longest_on_fire_team = None  

        total_player_success_rate = 0.0
        best_success_rate = { "team": None, "value": 0.0 } 

        most_epic_fail = {}
        most_epic_comeback = {} 

        for (id, player) in player_data.items(): 
            player_events = player.get_events()
            encoded_players.append(JSONEncoder().default(player))
            finalboard[id] = {
                "player_id": id,
                "name": player.name,
                "score": player.score,
                "longest_streak": player.longest_streak,
                "success_ratio": scoreboard.current_total_correct(player)
                / (scoreboard.total_requests_for(player) if scoreboard.total_requests_for(player) > 0 else 1),
            }

            total_requests += scoreboard.total_requests_for(player)
            
            total_streak_length = 0
            total_num_of_streaks = 0
            is_on_streak = False
            curr_streak_length = 0 

            player_success_rate = scoreboard.current_total_correct(player) / scoreboard.total_requests_for(player)
            total_player_success_rate += player_success_rate

            if player_success_rate > best_success_rate["value"]:
                best_success_rate["team"] = player.name
                best_success_rate["value"] = player_success_rate

            for (i, event) in enumerate(player_events):
                if is_on_streak and event.points_gained < 0: 
                    total_streak_length += curr_streak_length
                    total_num_of_streaks += 1

                    if curr_streak_length > 6: # was on fire 
                        strk_duration  = (event.timestamp - player_events[i-curr_streak_length].timestamp).total_seconds()

                        total_on_fire_duration += strk_duration
                        total_num_of_on_fires += 1

                        if curr_streak_length > longest_streak_length: 
                            longest_fire_duration = strk_duration
                            logest_on_fire_team = player.name

                    longest_streak_length = max(longest_streak_length, curr_streak_length)

                    curr_streak_length = 0
                    is_on_streak = False

                elif event.points_gained > 0:
                    curr_streak_length += 1

                    if not is_on_streak and curr_streak_length >= 2:
                        is_on_streak = True 
                    
            total_player_avg_streak += total_streak_length / (total_num_of_streaks if total_num_of_streaks > 0 else 1)        

        # Log game global stats
        stats["total_requests"] = total_requests
        stats["average_streak"] = total_player_avg_streak / num_players

        if total_num_of_on_fires > 0: 
            stats["average_on_fire_duration"] = average_on_fire_duration 
        else: 
            stats["average_on_fire_duration"] = "N/A"

        stats["longest_on_fire_duration"] = {
            "achieved_by_team" : longest_on_fire_team,
            "duration" : longest_on_fire_duration,
            "streak_len": longest_streak_length
        }

        stats["longest_streak"] = {
            "streak_len" : longest_streak_length,
            "duration" : longest_on_fire_duration
        }

        stats["average_success_rate"] = total_player_success_rate / num_players

        # Log game analysis 

        # Upload game data + review/analysis
        self.upload_data(
            game_id,
            encoded_players,
            finalboard=finalboard,
            finalgraph=finalgraph,
            stats=stats,
            analysis=analysis,
        )

    def upload_data(self, game_id, players_data, **reviews_items):
        
        self.db_client.xs[f"{game_id}_players"].insert_many(players_data)
        self.db_client.xs[f"{game_id}_review"].insert_many(
            [{"item": k, "stats": v} for k, v in reviews_items.items()]
        )
