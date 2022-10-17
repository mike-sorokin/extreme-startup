import json 
from flaskr.player import Player

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Player):
            return dict(name=obj.name, url=obj.url)
        return super().default(obj)