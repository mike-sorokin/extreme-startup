import datetime
from flaskr.shared.question_factory import QuestionFactory
from flaskr.shared.rate_controller import RateController

# Unique to each player. Responsible for sending questions to user api endpoint at frequency determined by rate_controller
# and incrementing player score in scoreboard
class QuizMaster:
    def __init__(
        self,
        player,
        question_factory,
        scoreboard,
        rate_controller=RateController(),
    ):
        self.player = player
        self.rate_controller = rate_controller
        self.question_factory = question_factory
        self.scoreboard = scoreboard
        self.is_warmup = self.question_factory.round == 0

    # Continuous loop, administering questions to self.player at a rate specified by RateController
    # Every question, check if game is over. If yes, then exit the thread.
    def start(self, warmup_over, running):
        # Init score as 0
        self.scoreboard.running_totals.append(
            {
                "time": datetime.datetime.now(datetime.timezone.utc),
                f"{self.player.uuid}": 0,
            }
        )

        while self.player.active: # NOTE: game.ended => not player.active
            self.administer_question(warmup_over, running)

    # Administer question involving:
    # (1) acquiring r_lock,
    # (2) send question to user HTTP get,
    # (3) adjust scoreboard/rate_controller based on response
    def administer_question(self, warmup_over, running):
        if self.is_warmup and warmup_over.is_set():
            self.is_warmup = False
            # Reset score to 0 once warmup ends
            self.scoreboard.running_totals.append(
                {
                    "time": datetime.datetime.now(datetime.timezone.utc),
                    f"{self.player.uuid}": 0,
                }
            )
            self.reset_stats_and_rc()

        question = self.question_factory.next_question()

        question.ask(self.player)

        self.scoreboard.record_request_for(self.player)
        self.scoreboard.increment_score_for(self.player, question)
        self.rate_controller.wait_for_next_request(question, warmup_over)
        self.rate_controller = self.rate_controller.update_algorithm_based_on_score(
            self.scoreboard.current_score(self.player)
        )

        running.wait() # Wait until running event is set to True -- i.e. when game is unpaused 

    def reset_stats_and_rc(self):
        self.player.streak = ""
        self.player.round_index = 0
        self.scoreboard.reset_player(self.player)
        self.rate_controller.reset()

    def player_passed(self):
        pass
