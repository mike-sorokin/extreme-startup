from flaskr.questions import *
import random

QUESTION_TYPES = [
    WarmupQuestion,
    AdditionQuestion,
    MaximumQuestion,
    MultiplicationQuestion,
    SquareCubeQuestion,
    PrimesQuestion,
    SubtractionQuestion,
    PowerQuestion,
    AdditionAdditionQuestion,
    AdditionMultiplicationQuestion,
    MultiplicationAdditionQuestion,
    AnagramQuestion,
    ScrabbleQuestion,
]

MAX_ROUND = len(QUESTION_TYPES) // 2

# QuestionFactory is unique to each game and generates questions within a window range dependent on round
class QuestionFactory:
    def __init__(self, round=1):
        self.round = round
        self.question_types = QUESTION_TYPES
        self.adjust_window()

    # Randomly select question from question window to ask player. Window size <= 4
    def next_question(self):
        available_question_types = self.question_types[
            self.window_start : self.window_end
        ]
        return random.choice(available_question_types)()

    # Adjust window to send differnt questions for next round
    def advance_round(self):
        self.round += 1
        self.adjust_window()

    def adjust_window(self):
        # If round is 0, set bound to 0:1 (only warmup question)
        # Otherwise, make sure to limit lower bound to 1 to avoid asking warmup q
        if self.round == 0:
            self.window_start = 0
            self.window_end = 1
        else:
            self.window_end = min(len(QUESTION_TYPES), self.round * 2 + 1)
            self.window_start = max(1, self.window_end - 4)

    def total_rounds(self):
        return MAX_ROUND
