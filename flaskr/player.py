from curses import noecho
from uuid import uuid4

# Player object -- NOTE: all player objects are associated with a game_id
class Player:
    def __init__(self, game_id, name, api):
        self.uuid = uuid4().hex[:8]
        self.game_id = game_id
        self.name = name

        self.score = 0

        self.api = api
        self.events = []

        self.active = True
        self.round_index = 0

        self.streak = ""
        self.curr_streak_length = 0
        self.longest_streak = 0  # for post-game-analysis

    def log_event(self, event):
        self.events.append(event)

    def __str__(self):
        return f"{self.name} ({self.api})"
