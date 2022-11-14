from uuid import uuid4
from flaskr.question_factory import QuestionFactory
from flaskr.scoreboard import Scoreboard
import threading
import time

ADVANCE_RATIO = 0.2

# 1 -> Correct
# X -> Wrong/Incorrect
# 0 -> No server response
STREAK_CHARS = ["1", "X", "0"]


class GamesManager:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(GamesManager, cls).__new__(cls)
            cls.instance.games = {}
        return cls.instance

    def get_all_games(self):
        return self.games

    def get_game(self, game_id):
        if game_id not in self.game:
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

    def game_has_password(self, game_id, password):
        return self.games[game_id].compare_password(password)

    def game_in_last_round(self, game_id):
        return self.games[game_id].is_last_round()

    def delete_games(self, *game_id):
        # Delete all game in game_id; if game_id is not provided, delete all games
        gids = game_id if game_id else self.games.keys
        for gid in list(gids):
            self.games[gid].remove_all_players()
            self.games[gid].pause()
            del self.games[gid]


# Most fundamental object in application -- stores information of players, scoreboard, questions gen., etc.
class Game:
    def __init__(self, admin_password, round=0):
        self.id = uuid4().hex[:8]
        self.admin_password = admin_password

        self.players = {}
        self.scoreboard = Scoreboard()
        self.question_factory = QuestionFactory(round)
        self.round = round

        self.first_round_event = threading.Event()
        self.ended = False

        self.running = threading.Event()
        self.running.set()

        self.players_to_assist = []
        self.auto_mode = False

    def compare_password(self, password):
        return password == self.admin_password

    def is_running(self):
        return self.running.is_set()

    def is_last_round(self):
        return self.round == self.question_factory.total_rounds()

    def new_player(self, player_id):
        self.players.append(player_id)

    # Automatation of round advancement & "Player-in-need" identification
    # Aim of this monitor:
    #   (1) Identify teams that are finding current round "too easy",
    #   (2) balance catching-up after a drought of points vs. escaping with the lead.
    # In the latter case we would want to increment round. Also in charge of informing game administrators
    def monitor(self):
        while self.running.is_set():
            num_players = len(self.players)
            if num_players != 0:
                if self.auto_mode and self.round != 0:
                    self.__auto_increment_round()
                self.__update_players_to_assist()

            time.sleep(2)

    def advance_round(self):
        self.question_factory.advance_round()
        self.round += 1
        self.first_round_event.set()

        for pid in self.players:
            self.players[pid].round_index = 0

    def is_last_round(self):
        return self.round == self.max_round

    def pause(self):
        self.running.clear()

    def unpause(self):
        self.running.set()

    def remove_all_players(self):
        pass

    def spawn_game_monitor(self):
        game_monitor_thread = threading.Thread(
            target=self.monitor, args=[self.players_dict, self.scoreboard]
        )
        game_monitor_thread.daemon = True  # for test termination
        game_monitor_thread.start()

    def __update_players_to_assist(self):
        for pid in self.players:
            curr_player = self.players[pid]
            streak, round_index = curr_player.streak, curr_player.round_index
            round_streak = streak[-round_index:] if round_index != 0 else ""

            # corect and incorrect tail(s)
            c_tail, ic_tail = (
                streak_length(round_streak, STREAK_CHARS[0]),
                streak_length(round_streak, "".join(STREAK_CHARS[1:])),
            )

            if c_tail > 0 and pid in self.players_to_assist:
                self.players_to_assist.remove(pid)

            elif ic_tail > 15 and pid not in self.players_to_assist:
                self.players_to_assist.append(pid)

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
