class QuizMaster:
    def __init__(self, player, question_factory, scoreboard): 
        self.player = player
        #self.rate_controller = RateController()
        self.question_factory = question_factory
        self.scoreboard = scoreboard 
    

