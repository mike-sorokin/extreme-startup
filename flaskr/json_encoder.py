import datetime
import json
from flaskr.player import Player
from flaskr.event import Event
from flaskr.game import Game
from flaskr.game_analysis import AnalysisEvent
from flaskr.shared.question_factory import MAX_ROUND

# Encode application objects to JSON format to support REST api
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Player):
            return dict(
                id=obj.uuid,
                game_id=obj.game_id,
                name=obj.name,
                score=obj.score,
                api=obj.api,
                events=[self.default(e) for e in obj.events],
                streak=obj.streak,
            )
        elif isinstance(obj, Event):
            return dict(
                id=obj.event_id,
                player_id=obj.player_id,
                query=obj.query,
                difficulty=obj.difficulty,
                points_gained=obj.points_gained,
                response_type=obj.response_type,
                timestamp=obj.timestamp,
            )
        elif isinstance(obj, Game):
            return dict(
                id=obj.id,
                round=obj.round,
                max_round=MAX_ROUND,
                players=list(obj.players.keys()),
                paused=not obj.running.is_set(),
                players_to_assist=obj.players_to_assist,
                auto_mode=obj.auto_mode,
            )
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, AnalysisEvent):
            return dict(
                title=obj.get_title(),
                description=obj.get_description(),
                time=obj.get_time(),
                player_id=obj.get_player_id(),
            )

        return super().default(obj)
