from curses import noecho
import uuid


class Player:
    def __init__(self, game_id, name, api):
        self.uuid = str(uuid.uuid4())
        self.game_id = game_id
        self.name = name
        self.score = 0
        self.api = api
        self.events = []
        self.active = True

    def log_result(id, msg, point):
        pass

    def log_event(self, event):
        self.events.append(event)

    def __str__(self):
        return f"{self.name} ({self.api})"
