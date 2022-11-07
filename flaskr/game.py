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

            if num_players != 0 and self.round != 0:
                # Minimum relative correct streak length needed to be a "player ready to move on"
                # advance_threshold = None
                # if num_players < 2:
                #     advance_threshold = 1
                # elif num_players < 5:
                #     advance_threshold = 0.6
                # else:
                #     advance_threshold = 0.3

                # # Calculate the relative length of the recent correct streak
                # num_advancable = 0
                # for pid in self.players:
                #     # Ignore players that don't have a full length streak

                #     curr_player = players_dict[pid]
                #     streak = curr_player.streak
                #     if len(streak) < STREAK_LENGTH:
                #         continue

                #     # rfind returns -1 if not found
                #     correct_num_tail = (
                #         len(streak) - max(streak.rfind("X"), streak.rfind("0")) + 1
                #     )

                #     # max() is to avoid divZero errors
                #     if correct_num_tail / max(len(streak), 1) >= advance_threshold:
                #         num_advancable += 1

                # print(num_advancable)

                # if num_advancable / num_players > ADVANCE_RATIO:
                #     self.question_factory.advance_round()
                #     self.round += 1
                #     self.first_round_event.set()

                ratio_threshold = 0.4
                advancable_players = 0

                for pid in self.players:

                    curr_player = players_dict[pid]
                    position, round_streak = (
                        scoreboard.leaderboard_position(curr_player),
                        curr_player.streak[curr_player.round_index :],
                    )

                    print(curr_player.streak, curr_player.round_index)
                    correct_num_tail = (
                        len(round_streak)
                        - max(round_streak.rfind("X"), round_streak.rfind("0"))
                        - 1
                    )
                    print(round_streak, correct_num_tail)

                    if correct_num_tail >= 6 and position <= max(
                        0.6 * len(self.players), 1
                    ):
                        advancable_players += 1

                if advancable_players / len(self.players) > ratio_threshold:
                    self.question_factory.advance_round()
                    self.round += 1
                    self.first_round_event.set()

            time.sleep(2)
