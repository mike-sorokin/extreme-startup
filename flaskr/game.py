from uuid import uuid4
from flaskr.shared.question_factory import QuestionFactory
from flaskr.scoreboard import Scoreboard
from flaskr.quiz_master import QuizMaster
from flaskr.game_analysis import *
import threading
import time


ADVANCE_RATIO = 0.2

# 1 -> Correct
# X -> Wrong/Incorrect
# 0 -> No server response
STREAK_CHARS = ["1", "X", "0"]

GAME_ANALYSIS_MONITOR = [
    NewLeaderMonitor,
    NewLastPlayerMonitor,
    EpicComebackMonitor,
    EpicFailMonitor,
]

# Most fundamental object in application -- stores information of players, scoreboard, questions gen., etc.
class Game:
    def __init__(self, admin_password, round=0):
        self.id = uuid4().hex[:8]
        self.admin_password = admin_password

        # player_id -> Player
        self.players = {}
        self.scoreboard = Scoreboard()

        self.question_factory = QuestionFactory(round)
        self.round = round

        self.first_round_event = threading.Event()
        self.ended = False  # only toggle this variable once

        self.running = threading.Event()
        self.running.set()

        self.players_to_assist = { "needs_assistance": [], "being_assisted": [] }
        self.auto_mode = False

        self.analysis_monitors = [
            monitor(self.log_analysis_events, self.scoreboard)
            for monitor in GAME_ANALYSIS_MONITOR
        ]
        self.analysis_events = []

    def compare_password(self, password):
        return password == self.admin_password

    def is_running(self):
        return self.running.is_set()

    def is_last_round(self):
        return self.round == self.question_factory.total_rounds()

    def add_player(self, player):
        self.scoreboard.new_player(player)
        self.players[player.uuid] = player

        quiz_master = QuizMaster(
            player,
            self.question_factory,
            self.scoreboard,
        )

        player_thread = threading.Thread(
            target=quiz_master.start,
            args=(self.first_round_event, self.running),
        )

        player_thread.daemon = True  # for test termination
        player_thread.start()

        return player

    # Automatation of round advancement & "Player-in-need" identification
    # Aim of this monitor:
    #   (1) Identify teams that are finding current round "too easy",
    #   (2) balance catching-up after a drought of points vs. escaping with the lead.
    # In the latter case we would want to increment round. Also in charge of informing game administrators
    def monitor(self):
        while not self.ended and self.running.is_set():
            num_players = len(self.players)
            if num_players != 0:
                if self.auto_mode and self.round != 0:
                    self.__auto_increment_round()
                self.__update_players_to_assist()
                self.__monitor_analysis_events()

            time.sleep(2)

    def advance_round(self):
        self.question_factory.advance_round()
        self.round += 1
        self.first_round_event.set()

        for pid in self.players:
            self.players[pid].round_index = 0

    def is_last_round(self):
        return self.round == self.question_factory.total_rounds()

    def pause(self):
        self.running.clear()

    def unpause(self):
        self.running.set()

    def end(self):
        self.ended = True

    # Mark player as inactive. Thread will be killed automatically when target function returns
    def remove_players(self, *player_id):
        pids = player_id if player_id else self.players.keys()

        for pid in list(pids):
            assert pid in self.players

            self.players[pid].active = False
            del self.players[pid]

    # returns: dict { player_id -> Player }
    def get_players(self, *player_id):
        pids = player_id if player_id else self.players.keys()
        return {pid: self.players[pid] for pid in list(pids)}

    def update_player(self, player_id, name=None, api=None):
        if name:
            self.players[player_id].name = name

        if api:
            self.players[player_id].api = api

    def assist_player(self, player_name):
        assert player_name in self.players_to_assist["needs_assistance"]

        # needs_assistance -> being_assisted
        self.players_to_assist["needs_assistance"].remove(player_name)
        self.players_to_assist["being_assisted"].append(player_name)

    def spawn_game_monitor(self):
        game_monitor_thread = threading.Thread(target=self.monitor)
        game_monitor_thread.daemon = True  # for test termination
        game_monitor_thread.start()

    def get_player_events(self, player_id):
        return self.players[player_id].events

    def log_analysis_events(self, analysis_event):
        self.analysis_events.append(analysis_event)

    def __monitor_analysis_events(self):
        for monitor in self.analysis_monitors:
            monitor.check()

    def __update_players_to_assist(self):
        needs_assistance = self.players_to_assist["needs_assistance"]
        being_assisted = self.players_to_assist["being_assisted"]

        for pid in self.players:
            curr_player = self.players[pid]
            curr_name = curr_player.name
            streak, round_index = curr_player.streak, curr_player.round_index
            round_streak = streak[-round_index:] if round_index != 0 else ""

            # corect and incorrect tail(s)
            c_tail, ic_tail = (
                streak_length(round_streak, STREAK_CHARS[0]),
                streak_length(round_streak, "".join(STREAK_CHARS[1:])),
            )

            if c_tail > 0:
                try:
                    if curr_name in needs_assistance:
                        needs_assistance.remove(curr_name)
                    elif curr_name in being_assisted:
                        being_assisted.remove(curr_name) 
                except:
                    print("MONITOR THREAD: TRIED REMOVING " + curr_name + " FROM needs_assitance/being_assisted WHEN MAIN THREAD ATTEMPTED MODIFYING SAID LISTS. CONTINUING ON...")

            elif ic_tail > 15 and (curr_name not in needs_assistance and curr_name not in being_assisted):
                needs_assistance.append(curr_name)

    def __auto_increment_round(self):
        ratio_threshold = 0.4
        advancable_players = 0

        for pid in self.players:
            curr_player = self.players[pid]
            round_index = curr_player.round_index
            position, round_streak = (
                self.scoreboard.leaderboard_position(curr_player),
                curr_player.streak[-round_index:] if round_index != 0 else "",
            )

            c_tail = streak_length(round_streak, "1")

            if c_tail >= 6 and position <= max(0.6 * len(self.players), 1):
                advancable_players += 1

        if advancable_players / len(self.players) > ratio_threshold:
            self.advance_round()


def streak_length(response_history, streak_char):
    return len(response_history) - len(response_history.rstrip(streak_char))
