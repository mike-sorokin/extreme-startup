from flaskr.json_encoder import JSONEncoder

class GameStats:

    def __init__(self, players, scoreboard):
        self.players = players
        self.scoreboard = scoreboard

        self.encoded_players = []
        self.finalboard = []
        self.stats = {}

        self.__initialise_stats_vars() 

    def __initialise_stats_vars(self): 
        self.num_players = len(self.players)
        assert self.num_players > 0

        # Basic variable/accumulation-variable definition
        #  ...for total requests statistics
        self.total_requests = 0

        # ...for average_streak
        self.total_player_avg_streak = 0

        # ...for average_on_fire_duration
        self.total_on_fire_duration = 0
        self.total_num_of_on_fires = 0

        # ...for longest_on_fire_duration
        self.longest_streak_length = 0
        self.longest_on_fire_duration = 0
        self.longest_on_fire_team = None

        # ...for average_success_rate
        self.total_player_success_rate = 0.0

        # ...for best_success_rate
        self.best_success_rate = { "team": None, "value": 0.0 }

        # ...for most_epic_fail
        self.most_epic_fail = {}

        # ...for most_epic_comeback
        self.most_epic_comeback = {}
        
    def __generate_player_stats(self): 
        for (id, player) in self.players.items():
            player_events = player.get_events()

            self.encoded_players.append(JSONEncoder().default(player))

            self.finalboard.append({
                "player_id": id,
                "name": player.name,
                "score": player.score,
                "longest_streak": player.longest_streak,
                "success_ratio": self.scoreboard.current_total_correct(player)
                / (self.scoreboard.total_requests_for(player) if self.scoreboard.total_requests_for(player) > 0 else 1),
            })

            self.total_requests += self.scoreboard.total_requests_for(player)

            # for curr player's avg streak
            total_streak_length = 0
            total_num_of_streaks = 0
            is_on_streak = False
            curr_streak_length = 0

            # for curr player's success rate
            player_success_rate = self.scoreboard.current_total_correct(player) / (self.scoreboard.total_requests_for(player) if self.scoreboard.total_requests_for(player) > 0 else 1)
            self.total_player_success_rate += player_success_rate

            if player_success_rate >= self.best_success_rate["value"]:
                self.best_success_rate["team"] = player.name
                self.best_success_rate["value"] = player_success_rate

            for (i, event) in enumerate(player_events):
                if is_on_streak and (i + 1 == len(player_events) or event.points_gained < 0):  # qustion response wrong or error response
                    # curr_streak has ended!
                    # account for this and reset is_on_streak to false
                    curr_streak_length += int(i + 1 == len(player_events))
                    total_streak_length += curr_streak_length
                    total_num_of_streaks += 1

                    if curr_streak_length > 6: # player was on fire
                        strk_duration  = (event.timestamp - player_events[i - curr_streak_length + 1].timestamp).total_seconds()
                        self.total_on_fire_duration += strk_duration
                        self.total_num_of_on_fires += 1

                        if curr_streak_length > self.longest_streak_length:
                            self.longest_on_fire_duration = strk_duration
                            self.longest_on_fire_team = player.name

                    self.longest_streak_length = max(self.longest_streak_length, curr_streak_length)

                    # reset accum vars
                    curr_streak_length = 0
                    is_on_streak = False

                elif event.points_gained > 0: # player gets question correct
                    curr_streak_length += 1

                    if not is_on_streak and curr_streak_length >= 2:
                        is_on_streak = True

            if total_num_of_streaks > 0: # => total_streak_length > 0
                self.total_player_avg_streak += total_streak_length / total_num_of_streaks

    def __build_stats_dict(self):
        self.stats["num_players"] = self.num_players
        self.stats["total_requests"] = self.total_requests
        self.stats["average_streak"] = self.total_player_avg_streak / self.num_players

        if self.total_num_of_on_fires > 0:
            self.stats["average_on_fire_duration"] = self.total_on_fire_duration / self.total_num_of_on_fires

        if self.longest_on_fire_team:
            self.stats["longest_on_fire_duration"] = {
                "achieved_by_team" : self.longest_on_fire_team,
                "duration" : self.longest_on_fire_duration,
                "streak_len": self.longest_streak_length
            }

        self.stats["longest_streak"] = self.longest_streak_length
        self.stats["average_success_rate"] = self.total_player_success_rate / self.num_players

        if self.best_success_rate["team"]:
            self.stats["best_success_rate"] = self.best_success_rate

    def generate_game_stats(self):
        self.__generate_player_stats()
        self.__build_stats_dict() 
        return self.encoded_players, self.finalboard, self.stats 