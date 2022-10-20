from flaskr.questions import *
import random


class QuestionFactory:
    def __init__(self, round=1):
        self.round = round
        self.question_types = [
            WarmupQuestion,
            AdditionQuestion,
            SubtractionQuestion,
            PowerQuestion,
            AdditionAdditionQuestion,
            AdditionMultiplicationQuestion,
            MultiplicationAdditionQuestion,
            MaximumQuestion,
        ]

    def next_question(self):
        window_end = max(1, self.round * 2)
        window_start = max(0, window_end - 4)
        available_question_types = self.question_types[window_start:window_end]
        return random.choice(available_question_types)()

    def advance_round(self):
        self.round += 1
