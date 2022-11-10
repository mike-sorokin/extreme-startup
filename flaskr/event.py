from uuid import uuid4
import datetime as dt

# Event's stored for <player_id> to track historial of player responses
class Event:
    def __init__(
        self, player_id, game_id, query, difficulty, points_gained, response_type
    ):
        self.player_id = player_id
        self.game_id = game_id
        self.query = query
        self.difficulty = difficulty
        self.points_gained = points_gained
        self.response_type = response_type
        self.event_id = uuid4().hex[:8]
        self.timestamp = dt.datetime.now(dt.timezone.utc)

    def __str__(self):
        return f"""
        Player: {self.player_id},
        Game: {self.game_id},
        Query: {self.query},
        Difficulty: {self.difficulty}
        Points: {self.points_gained}
        Timestamp: {self.timestamp.isoformat()}
        """
