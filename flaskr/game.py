from uuid import uuid4
from flaskr.question_factory import QuestionFactory
from readerwriterlock import rwlock
import threading
import time

from flaskr.scoreboard import STREAK_LENGTH

ADVANCE_RATIO = 0.2

# Most fundamental object in application -- stores information of players, scoreboard, questions gen., etc.
class Game:
    def __init__(self, admin_password, round=0):
        self.id = uuid4().hex[:8]
        self.players = []
        self.round = round

        self.question_factory = QuestionFactory(round)
        self.first_round_event = threading.Event()

        self.paused = False
        pauser = rwlock.RWLockWrite()
        self.pause_rlock, self.pause_wlock = pauser.gen_rlock(), pauser.gen_wlock()

        self.admin_password = admin_password

        self.assists = []

        self.auto_mode = False

    def new_player(self, player_id):
        self.players.append(player_id)

    # Automatation of round advancement & "Player-in-need" identification
    # Aim of this monitor:
    #   (1) Identify teams that are finding current round "too easy",
    #   (2) balance catching-up after a drought of points vs. escaping with the lead.
    # In the latter case we would want to increment round. Also in charge of informing game administrators
    def monitor(self, players_dict, scoreboard):
        while not self.paused:

            num_players = len(self.players)

            if num_players != 0:
                if self.auto_mode and self.round != 0:
                    self.__auto_increment_round(players_dict, scoreboard)
                self.__monitor_assists(players_dict)

            time.sleep(2)

    def __monitor_assists(self, players_dict):
        for pid in self.players:
            curr_player = players_dict[pid]
            streak = curr_player.streak
            round_streak = streak[curr_player.round_index :]

            correct_num_tail = (
                len(round_streak)
                - max(round_streak.rfind("X"), round_streak.rfind("0"))
                - 1
            )
            wrong_num_tail = (
                len(round_streak)
                - max(round_streak.rfind("0"), round_streak.rfind("1"))
                - 1
            )
            no_response_num_tail = (
                len(streak) - max(streak.rfind("X"), streak.rfind("1")) - 1
            )

            if correct_num_tail > 0 and pid in self.assists:
                self.assists.remove(pid)
            elif (
                no_response_num_tail > 10 or wrong_num_tail > 15
            ) and pid not in self.assists:
                self.assists.append(pid)

    def __auto_increment_round(self, players_dict, scoreboard):
        ratio_threshold = 0.4
        advancable_players = 0

        for pid in self.players:
            curr_player = players_dict[pid]
            position, round_streak = (
                scoreboard.leaderboard_position(curr_player),
                curr_player.streak[curr_player.round_index :],
            )

            correct_num_tail = (
                len(round_streak)
                - max(round_streak.rfind("X"), round_streak.rfind("0"))
                - 1
            )

            if correct_num_tail >= 6 and position <= max(0.6 * len(self.players), 1):
                advancable_players += 1

        if advancable_players / len(self.players) > ratio_threshold:
            self.question_factory.advance_round()
            self.round += 1
            self.first_round_event.set()

            for pid in self.players:
                players_dict[pid].round_index = 0
