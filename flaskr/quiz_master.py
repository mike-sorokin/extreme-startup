import time
from flaskr.rate_controller import RateController

class QuizMaster:
    def __init__(self, player, question_factory, scoreboard, rate_controller = RateController()):
        self.player = player
        self.rate_controller = rate_controller
        self.question_factory = question_factory
        self.scoreboard = scoreboard 
    
    def start(self):
        while self.player.active:
            self.administer_question()
    
    def administer_question(self):
        question = self.question_factory.next_question()
        question.ask(self.player)
        self.scoreboard.record_request_for(self.player)
        self.scoreboard.increment_score_for(self.player, question)
        self.rate_controller.wait_for_next_request(question)
        self.rate_controller = self.rate_controller.update_algorithm_based_on_score(self.scoreboard.current_score(self.player))

    def player_passed(self):
        pass 