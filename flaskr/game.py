from uuid import uuid4
from flaskr.question_factory import QuestionFactory
from readerwriterlock import rwlock

# Most fundamental object in application -- stores information of players, scoreboard, questions gen., etc.
class Game:
    def __init__(self, admin_password, round=0):
        self.id = uuid4().hex[:8]
        self.players = []
        self.round = round
        self.question_factory = QuestionFactory(round)
        self.paused = False
        pauser = rwlock.RWLockWrite()
        self.pause_rlock, self.pause_wlock = pauser.gen_rlock(), pauser.gen_wlock()
        self.admin_password = admin_password

    def new_player(self, player_id):
        self.players.append(player_id)
