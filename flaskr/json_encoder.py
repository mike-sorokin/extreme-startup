import json
from flaskr.player import Player


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Player):
            return dict(
                id=obj.uuid,
                game_id=obj.game_id,
                name=obj.name,
                score=obj.score,
                api=obj.api,
                events=obj.events,
            )
        return super().default(obj)
