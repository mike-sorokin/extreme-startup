import time

class QuizMaster:
    def __init__(self, player, question_factory, scoreboard):
        self.player = player
        # self.rate_controller = RateController()
        self.question_factory = question_factory
        self.scoreboard = scoreboard 
    
    def start(self):
        while self.player.active:
            question = self.question_factory.next_question()
            question.ask(self.player)
            self.scoreboard.record_request_for(self.player)
            self.scoreboard.increment_score_for(self.player, question)
            time.sleep(5) # question_delay

    def player_passed(self):
        pass 