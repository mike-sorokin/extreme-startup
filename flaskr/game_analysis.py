import datetime
import time


class AnalysisEvent:
    def __init__(self, title, description, player_id):
        self.title = title
        self.description = description
        self.time = datetime.datetime.now().strftime("%b %d %H:%M:%S")
        self.player_id = player_id

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_time(self):
        return self.time

    def get_player_id(self):
        return self.player_id


class AnalysisMonitor:
    def __init__(self, log_func, scoreboard):
        self.log_func = log_func
        self.scoreboard = scoreboard

    # abstract function to be overwritten
    def check(self):
        pass


class NewLeaderMonitor(AnalysisMonitor):
    """
    Event monitor to check when a player become leader for more than 15 seconds.
    If check pass, log corresponding event. This monitor shouldn't log the same
    leader consecutively, and shouldn't log a new leader whose leader position is maintained
    for less than 15 secs.
    """

    DURATION_REQUIRED = 15

    def __init__(self, logger, scoreboard):
        super().__init__(logger, scoreboard)
        self.prev_leader = None
        self.curr_leader = None
        self.time_in = None

    def check(self):
        # reassign prev_player when new leader exists
        # INVARIANCE:
        #   (1) prev_leader == curr_leader when a new leader is established
        #   (2) At transition, prev_leader is assigned to old leader, new_leader to new leader
        if self.curr_leader != self.scoreboard.leaderboard_first_player_id():
            # To Transition State
            self.prev_leader = self.curr_leader
            self.curr_leader = self.scoreboard.leaderboard_first_player_id()
            self.time_in = time.time()
        elif (
            time.time() - self.time_in > NewLeaderMonitor.DURATION_REQUIRED
            and self.prev_leader != self.curr_leader
        ):
            # To Established State
            self.log_func(
                AnalysisEvent(
                    "New Leader",
                    f"Player {self.scoreboard.uuid_to_names.get(self.curr_leader, '???')} beat the previous leader and maintained that position for more than 15 seconds",
                    self.curr_leader,
                )
            )
            self.prev_leader = self.curr_leader


class NewLastPlayerMonitor(AnalysisMonitor):
    """
    Event monitor to check when a player become leader for more than 15 seconds.
    If check pass, log corresponding event. This monitor shouldn't log the same
    leader consecutively, and shouldn't log a new leader whose leader position is maintained
    for less than 15 secs.
    """

    DURATION_REQUIRED = 15

    def __init__(self, logger, scoreboard):
        super().__init__(logger, scoreboard)
        self.curr_last = None
        self.prev_last = None
        self.time_in = None

    def check(self):
        # reassign prev_last when new last player exists
        # INVARIANCE:
        #   (1) prev_last == curr_last when a new last player is established
        #   (2) At transition, prev_last is assigned to old last player, new_last to new last player
        if self.curr_last != self.scoreboard.leaderboard_last_player_id():
            self.prev_last = self.curr_last
            self.curr_last = self.scoreboard.leaderboard_last_player_id()
            self.time_in = time.time()
        elif (
            time.time() - self.time_in > NewLastPlayerMonitor.DURATION_REQUIRED
            and self.prev_last != self.curr_last
        ):
            self.log_func(
                AnalysisEvent(
                    "New Leader",
                    f"Player {self.scoreboard.uuid_to_names.get(self.prev_last, '???')} became the worst one and maintained that position for more than 15 seconds",
                    self.prev_last,
                )
            )
            self.prev_last = self.curr_last


class EpicComebackMonitor(AnalysisMonitor):
    """
    Event monitor to check when a player climb in ranking from bottom 20 percentile to top 20
    percentile and remain in the top 20 percentile for more than 5 seconds. The climb itself can happens
    gradually over a long period of time. If check pass, log corresponding event.
    """

    DURATION_REQUIRED = 5

    def __init__(self, logger, scoreboard):
        super().__init__(logger, scoreboard)
        self.potential_players = dict()  # player_id -> lowest_score
        self.transition_players = (
            dict()
        )  # player_id -> {"worst": (int), "time_in": (datetime)}

    def check(self):
        # INVARIANCE: Player are can't be in potential_players and transition_players at the same time
        for pid in self.scoreboard.leaderboard_bottom_k_percentile_players(20):
            try:
                curr_pos = self.scoreboard.leaderboard_position_id(pid)
            except ValueError:
                continue

            if pid in self.potential_players:
                self.potential_players[pid] = max(self.potential_players[pid], curr_pos)
            else:
                self.potential_players[pid] = curr_pos

        for pid, lowest_score in list(self.potential_players.items()):
            try:
                player_in_top_percentile = self.scoreboard.player_in_top_k_percentile(
                    pid, 20
                )
            except ValueError:
                del self.potential_players[pid]
                continue

            if player_in_top_percentile:
                self.transition_players[pid] = {
                    "worst": lowest_score,
                    "time_in": time.time(),
                }
                del self.potential_players[pid]

        for pid, entry in list(self.transition_players.items()):
            try:
                player_in_top_percentile = self.scoreboard.player_in_top_k_percentile(
                    pid, 20
                )
            except KeyError:
                del self.transition_players[pid]
                continue

            if not player_in_top_percentile:
                self.potential_players[pid] = entry["worst"]
                del self.transition_players[pid]
            elif time.time() - entry["time_in"] > EpicComebackMonitor.DURATION_REQUIRED:
                self.log_func(
                    AnalysisEvent(
                        "Epic Comeback",
                        f"Player {self.scoreboard.uuid_to_names.get(pid, '???')} started his epic comeback which was at least 5 seconds long",
                        pid,
                    )
                )
                del self.transition_players[pid]


class EpicFailMonitor(AnalysisMonitor):
    """
    Event monitor to check when a player fall in ranking from top 20 percentile to bottom 20
    percentile and remain in the bottom 20 percentile for more than 5 seconds. The fall itself can happens
    gradually over a long period of time. If check pass, log corresponding event.
    """

    DURATION_REQUIRED = 5

    def __init__(self, logger, scoreboard):
        super().__init__(logger, scoreboard)
        self.potential_players = dict()  # player_id -> highest_score
        self.transition_players = (
            dict()
        )  # player_id -> {"best": (int), "time_in": (datetime)}

    def check(self):
        # INVARIANCE: Player are can't be in potential_players and transition_players at the same time
        for pid in self.scoreboard.leaderboard_top_k_percentile_players(20):
            try:
                curr_pos = self.scoreboard.leaderboard_position_id(pid)
            except ValueError:
                continue

            if pid in self.potential_players:
                self.potential_players[pid] = min(self.potential_players[pid], curr_pos)
            else:
                self.potential_players[pid] = curr_pos

        for pid, highest_score in list(self.potential_players.items()):
            try:
                player_in_bottom_percentile = (
                    self.scoreboard.player_in_bottom_k_percentile(pid, 20)
                )
            except ValueError:
                del self.potential_players[pid]
                continue

            if player_in_bottom_percentile:
                self.transition_players[pid] = {
                    "best": highest_score,
                    "time_in": time.time(),
                }
                del self.potential_players[pid]

        for pid, entry in list(self.transition_players.items()):
            try:
                player_in_bottom_percentile = (
                    self.scoreboard.player_in_bottom_k_percentile(pid, 20)
                )
            except KeyError:
                del self.transition_players[pid]
                continue

            if not player_in_bottom_percentile:
                self.potential_players[pid] = entry["best"]
                del self.transition_players[pid]
            elif time.time() - entry["time_in"] > EpicFailMonitor.DURATION_REQUIRED:
                self.log_func(
                    AnalysisEvent(
                        "Epic Fail",
                        f"Player {self.scoreboard.uuid_to_names.get(self.pid, '???')} started his epic fail which was at least 5 seconds long",
                        pid,
                    )
                )
                del self.transition_players[pid]
