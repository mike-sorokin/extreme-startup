from flaskr.questions import WarmupQuestion, AdditionQuestion, SubtractionQuestion

class QuestionFactory:
    def __init__(self, round=1):
        self.round = round
        self.question_types = [WarmupQuestion, AdditionQuestion, SubtractionQuestion]

    def next_question(self):
        print(type(self.question_types[self.round]()))
        return self.question_types[self.round]()

    def advance_round(self):
        self.round += 1