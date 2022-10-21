from uuid import uuid4
from flaskr.question_factory import QuestionFactory

class Game:
    def __init__(self, round=0):
        self.id = str(uuid4())
        self.players = []
        self.round = round
        self.question_factory = QuestionFactory(round) 

    def new_player(self, player_id):
        self.players.append(player_id)