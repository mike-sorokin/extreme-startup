from uuid import uuid4

class Game:
    def __init__(self, round=0):
        self.id = str(uuid4())
        self.round = round
        self.players = []
    #   self.question_factory = QuestionFactory() 

    def add_player(player):
        players.append(player)