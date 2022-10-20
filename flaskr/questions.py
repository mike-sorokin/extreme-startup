import numbers
from uuid import uuid4
import random
import yaml
import os


class Question:
    def __init__(self, points=10):
        self.uuid = str(uuid4())
        self.points = points
        self.answer = None
        self.result = ""
        self.problem = ""

    def ask(self, player):
        try:
            response = requests.get(player.api, params={"q": self.as_text()})

            if response.status_code == 200:
                self.answer = response.text.strip().lower()
            else:
                self.problem = "ERROR_RESPONSE"

        except Exception:
            self.problem = "NO_SERVER_RESPONSE"
        self.get_result()

    def get_result(self):
        if self.answer is None:
            self.result = self.problem
        elif self.answered_correctly():
            self.result = "CORRECT"
        else:
            self.result = "WRONG"

    def delay_before_next(self):
        if self.result == "CORRECT":
            return 5
        elif self.result == "WRONG":
            return 10
        else:
            return 20

    def display_result(self):
        return f"\tQuestion: {self.__str__}\n\tAnswer: {self.answer}\n\tResult: {self.result}"

    def __str__(self):
        return f"{self.uuid}: {self.as_text()}"

    def as_text(self):
        return "Basic Question Class"

    def answered_correctly(self):
        return self.answer == self.correct_answer()

    def correct_answer(self):
        pass


class WarmupQuestion(Question):
    def __init__(self, player_name="default_name"):
        self.player_name = player_name
        super().__init__()

    def correct_answer(self):
        return self.player_name

    def as_text(self):
        return "What is your name?"


class UnaryyMathsQuestion(Question):
    def __init__(self, *number):
        super().__init__()
        if valid_num_arguments(1, number):
            self.number = number[0]
        else:
            self.number = random.randint(1, 100)


class BinaryMathsQuestion(Question):
    def __init__(self, *numbers):
        super().__init__()
        if valid_num_arguments(2, numbers):
            self.n1 = numbers[0]
            self.n2 = numbers[1]
        else:
            self.n1 = random.randint(1, 100)
            self.n2 = random.randint(1, 100)


class TernaryMathsQuestion(Question):
    def __init__(self, *numbers):
        super().__init__()
        if valid_num_arguments(3, numbers):
            self.n1, self.n2, self.n3 = numbers
        else:
            self.n1, self.n2, self.n3 = random.sample(range(1, 100), 3)


class SelectFromListOfNumbersQuestion(Question):
    def __init__(self, *numbers):
        super().__init__()
        if len(numbers) != 0 and valid_num_arguments(len(numbers), numbers):
            self.numbers = numbers
        else:
            size = random.randint(1, 5)
            self.numbers = random.sample(range(1, 100), size)

    def correct_answer(self):
        return super().correct_answer()


class MaximumQuestion(SelectFromListOfNumbersQuestion):
    def __init__(self, *numbers):
        super().__init__(*numbers)
        self.points = 40

    def as_text(self):
        return f"which of the following numbers is the largest: {', '.join(map(str, self.numbers))}"

    def correct_answer(self):
        return max(self.numbers)


class AdditionQuestion(BinaryMathsQuestion):
    def as_text(self):
        return f"What is {self.n1} plus {self.n2}"

    def correct_answer(self):
        return self.n1 + self.n2


class SubtractionQuestion(BinaryMathsQuestion):
    def as_text(self):
        return f"What is {self.n1} minus {self.n2}"

    def correct_answer(self):
        return self.n1 - self.n2


class MultiplicationQuestion(BinaryMathsQuestion):
    def as_text(self):
        return f"What is {self.n1} multiplied by {self.n2}"

    def correct_answer(self):
        return self.n1 * self.n2


class AdditionAdditionQuestion(TernaryMathsQuestion):
    def __init__(self, *numbers):
        super().__init__(*numbers)
        self.points = 30

    def as_text(self):
        return f"What is {self.n1} plus {self.n2} plus {self.n3}"

    def correct_answer(self):
        return self.n1 + self.n2 + self.n3


class AdditionMultiplicationQuestion(TernaryMathsQuestion):
    def __init__(self, *numbers):
        super().__init__(*numbers)
        self.points = 60

    def as_text(self):
        return f"What is {self.n1} plus {self.n2} multiplied by {self.n3}"

    def correct_answer(self):
        return self.n1 + self.n2 * self.n3


class MultiplicationAdditionQuestion(TernaryMathsQuestion):
    def __init__(self, *numbers):
        super().__init__(*numbers)
        self.points = 50

    def as_text(self):
        return f"What is {self.n1} multiplied by {self.n2} plus {self.n3}"

    def correct_answer(self):
        return self.n1 * self.n2 + self.n3


class PowerQuestion(BinaryMathsQuestion):
    def __init__(self, *numbers):
        super().__init__(*numbers)
        self.points = 50

    def as_text(self):
        return f"What is {self.n1} to the power of {self.n2}"

    def correct_answer(self):
        return self.n1**self.n2


class SquareCubeQuestion(SelectFromListOfNumbersQuestion):
    def __init__(self, *numbers):
        super().__init__(*numbers)
        self.points = 50

    def as_text(self):
        return f"which of the following numbers is both a square and a cube: {', '.join(map(str, self.numbers))}"

    def correct_answer(self):
        is_square_cube = (
            lambda x: round(x ** (1 / 3)) ** 3 == x and round(x ** (1 / 3)) ** 3 == x
        )
        return ", ".join(map(str, filter(is_square_cube, self.numbers)))


class PrimesQuestion(SelectFromListOfNumbersQuestion):
    def __init__(self, *numbers):
        super().__init__(*numbers)
        self.points = 60

    def as_text(self):
        return f"which of the following numbers are primes: {', '.join(map(str, self.numbers))}"

    def correct_answer(self):
        is_prime = (
            lambda x: all([(x % j) for j in range(2, int(x**0.5) + 1)]) and x > 1
        )
        return ", ".join(map(str, filter(is_prime, self.numbers)))


class FibonacciQuestion(UnaryyMathsQuestion):
    def __init__(self, *numbers):
        super().__init__(*numbers)
        self.points = 50

    def ordinal(self, number):
        last_digit = number % 10
        if number in [11, 12, 13]:
            return "th"
        if last_digit == 1:
            return "st"
        elif last_digit == 2:
            return "nd"
        elif last_digit == 3:
            return "rd"
        else:
            return "th"

    def as_text(self):
        return f"what is the {str(self.number) + self.ordinal(11)} number in the Fibonacci sequence"

    def fib(n):
        a, b = 0, 1
        for i in range(n):
            a, b = b, a + b
        return a

    def correct_answer(self):
        return FibonacciQuestion.fib(self.number)


class GeneralKnowledgeQuestion(Question):
    def __init__(self, question="", answer=""):
        super().__init__
        if question == "" or answer == "":
            with open("flaskr/general_knowledge.yaml", "r") as infile:
                quiz_cards = yaml.safe_load(infile)
            card = random.choice(quiz_cards)
            self.question = card["question"]
            self.answer = card["answer"]
        else:
            self.question = question
            self.answer = answer

    def as_text(self):
        return self.quesion

    def correct_answer(self):
        return self.answer


class AnagramQuestion(Question):
    def __init__(self, anagram="", correct="", incorrect=[]):
        super().__init__
        if anagram == "" or correct == "" or len(incorrect) == 0:
            with open("flaskr/anagrams.yaml", "r") as infile:
                anagrams = yaml.safe_load(infile)
            anagram = random.choice(anagrams)
            self.anagram, self.correct, self.incorrect = anagram.values()
        else:
            self.anagram, self.correct, self.incorrect = anagram, correct, incorrect

    def as_text(self):
        possible_words = [self.correct] + self.incorrect
        return f"which of the following is an anagram of {anagram}: {', '.join(random.shuffle(possible_words))}"

    def correct_answer(self):
        return self.correct


class ScrabbleQuestion(Question):
    def __init__(self, word=""):
        super().__init__()
        if word == "":
            self.word = random.choice(
                ["banana", "september", "cloud", "zoo", "ruby", "buzzword"]
            )
        else:
            self.word = word.lower()

    def as_text(self):
        return f"what is the scrabble score of {self.word}"

    def score(word):
        score = 0
        for c in word:
            if c in "eaionrtlsu":
                score += 1
            elif c in "dg":
                score += 2
            elif c in "bcmp":
                score += 3
            elif c in "fhvw":
                score += 4
            elif c in "k":
                score += 5
            elif c in "jx":
                score += 8
            elif c in "qz":
                score += 0
        return score

    def correct_answer(self):
        return ScrabbleQuestion.score(self.word)


def valid_num_arguments(arg_num, numbers):
    return len(list(numbers)) == arg_num and all(
        isinstance(num, int) for num in numbers
    )
