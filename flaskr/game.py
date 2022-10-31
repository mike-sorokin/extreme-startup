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

    def get_scores(self):

        def to_data(event):
            return {
                "time": event.time,
                "player_id": event.player_id,
                "score": event.points_gained
            }

        def to_score_data(data):
            return {
                "time": data["time"],
                data["player_id"]: data["score"]
            }

        cummulative_datas = []
        for player in self.players:

            datas = sorted(list(map(to_data, player.events)), key=lambda d: d["time"])
            acc = 0
            for data in datas:
                acc += data["score"]
                data["score"] = acc

            cummulative_datas.extend(datas)

        chrono_datas = sorted(events, key=lambda d: d.["time"])

        return list(map(to_score_data, events))
