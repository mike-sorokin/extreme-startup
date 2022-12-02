from flaskr.shared.questions import *
import random

QUESTION_TYPES = [
    WarmupQuestion,
    AdditionQuestion,
    MaximumQuestion,
    MultiplicationQuestion,
    SquareCubeQuestion,
    GeneralKnowledgeQuestion,
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
    def __init__(self):
        self.question_types = QUESTION_TYPES

    # Randomly select question from question window to ask player. Window size <= 4
    def next_question(self, round):
        window_start, window_end = self.adjust_window(round) 
        available_question_types = self.question_types[
            window_start : window_end
        ]
        return random.choice(available_question_types)()

    def adjust_window(self, round):
        window_end = max(1, round * 2)
        window_start = max(0, window_end - 4)
        return (window_start, window_end) 

    def total_rounds(self):
        return MAX_ROUND
