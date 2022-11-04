import datetime
from flaskr.question_factory import QuestionFactory
from flaskr.rate_controller import RateController

# Unique to each player. Responsible for sending questions to user api endpoint at frequency determined by rate_controller
# and incrementing player score in scoreboard
class QuizMaster:
    def __init__(
        self,
        player,
        question_factory,
        scoreboard,
        rlock,
        rate_controller=RateController(),
    ):
        self.player = player
        self.rate_controller = rate_controller
        self.question_factory = question_factory
        self.scoreboard = scoreboard
        self.rlock = rlock
        self.is_warmup = self.question_factory.round == 0

    # Continuous loop, administering questions to self.player at a rate specified by RateController
    def start(self, e):
        while self.player.active:
            self.administer_question(e)

    # Administer question involving:
    # (1) acquiring r_lock,
    # (2) send question to user HTTP get,
    # (3) adjust scoreboard/rate_controller based on response
    def administer_question(self, warmup_over):
        if self.is_warmup and warmup_over.is_set():
            self.is_warmup = False
            self.scoreboard.running_totals.append(
                {
                    "time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    f"{self.player.uuid}": 0,
                }
            )
            self.reset_stats_and_rc()

        question = self.question_factory.next_question()

        self.rlock.acquire()  # If wlock acquired (paused), sleep here until wlock released. Many rlock acquires possible for players
        question.ask(self.player)

        if self.rlock.locked():
            self.rlock.release()

        self.scoreboard.record_request_for(self.player)
        self.scoreboard.increment_score_for(self.player, question)
        self.rate_controller.wait_for_next_request(question, warmup_over)
        self.rate_controller = self.rate_controller.update_algorithm_based_on_score(
            self.scoreboard.current_score(self.player)
        )

    def reset_stats_and_rc(self):
        self.player.streak = ""
        self.scoreboard.reset_player(self.player)
        self.rate_controller.reset()

    def player_passed(self):
        pass
