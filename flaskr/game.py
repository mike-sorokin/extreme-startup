from uuid import uuid4
from flaskr.question_factory import QuestionFactory
from readerwriterlock import rwlock
import threading
import time

# Most fundamental object in application -- stores information of players, scoreboard, questions gen., etc.
class Game:
    def __init__(self, admin_password, round=0):
        self.id = uuid4().hex[:8]
        self.players = []
        self.round = round

        self.question_factory = QuestionFactory(round)
        self.first_round_event = threading.Event()

        self.paused = False
        pauser = rwlock.RWLockWrite()
        self.pause_rlock, self.pause_wlock = pauser.gen_rlock(), pauser.gen_wlock()
        
        self.admin_password = admin_password

    def new_player(self, player_id):
        self.players.append(player_id)
    
    # Automatation of round advancement 
    # Aim of this monitoring-bot: (1) Identify teams that are finding current round "too easy", (2) balance catching-up after a drought of points vs.
    # escaping with the lead. In the latter case we would want to increment round. 
    def monitor(self):
        while not self.paused:
            time.sleep(5) 