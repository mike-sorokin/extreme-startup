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
        self.streak = ""
        self.round_index = 0

    def log_event(self, event):
        self.events.append(event)

    def __str__(self):
        return f"{self.name} ({self.api})"
