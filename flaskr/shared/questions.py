import numbers
from uuid import uuid4
import requests
import random
import yaml
import os
import requests

ALLOW_CHEATING = True

# Basic question object. Questions asked to players are instances of subclasses. Should be treated as abstract class
class Question:
    def __init__(self, points=10):
        self.uuid = uuid4().hex[:8]
        self.points = points
        self.answer = None
        self.result = ""
        self.problem = ""

    # Ask player a question and store the result/problem in attribute
    def ask(self, player):
        if isinstance(self, WarmupQuestion):
            self.player_name = player.name.strip().lower()

        try:
            response = requests.get(player.api, params={"q": self.as_text()})

            if response.status_code == 200:
                self.answer = response.text.strip().lower()
            else:
                self.problem = "ERROR_RESPONSE"

        except Exception:
            self.problem = "NO_SERVER_RESPONSE"

        self.get_result()

    # Store answer result in attribute
    def get_result(self):
        if self.answer is None:
            self.result = self.problem

        elif ALLOW_CHEATING and self.answer == "cheat":
            self.result = "CORRECT"

        elif self.answered_correctly():
            self.result = "CORRECT"

        else:
            self.result = "WRONG"

    # Delay interval depending on result
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

    # abstract function to be overwritten
    def as_text(self):
        return "Basic Question Class"

    # Check the player answered correctly
    def answered_correctly(self):
        return self.answer == str(self.correct_answer())

    # abstract function to be overwritten
    def correct_answer(self):
        pass


# A warmup question which ask players's name
class WarmupQuestion(Question):
    def __init__(self, player_name="default_name"):
        self.player_name = player_name
        super().__init__()

    def correct_answer(self):
        return self.player_name

    def as_text(self):
        return "What is your name?"


# An abstract class which involve a number, generating a random number if number
# not provided during construction
class UnaryyMathsQuestion(Question):
    def __init__(self, *number):
        super().__init__()
        if valid_num_arguments(1, number):
            self.number = number[0]

        else:
            self.number = random.randrange(1, 100)


# An abstract question class which involve two numbers, generating two random number if numbers
# not provided during construction
class BinaryMathsQuestion(Question):
    def __init__(self, *numbers):
        super().__init__()
        if valid_num_arguments(2, numbers):
            self.n1 = numbers[0]
            self.n2 = numbers[1]

        else:
            self.n1 = random.randrange(1, 100)
            self.n2 = random.randrange(1, 100)


# An abstract question class which involve three numbers, generating three random number if numbers
# not provided during construction
class TernaryMathsQuestion(Question):
    def __init__(self, *numbers):
        super().__init__()
        if valid_num_arguments(3, numbers):
            self.n1, self.n2, self.n3 = numbers

        else:
            self.n1, self.n2, self.n3 = random.sample(range(1, 100), 3)


# An abstract question class which involve list of numbers, generating list of random number
# of lenght 1 to 9 if numbers not provided during construction
class SelectFromListOfNumbersQuestion(Question):
    def __init__(self, *numbers):
        super().__init__()
        if len(numbers) != 0 and valid_num_arguments(len(numbers), numbers):
            self.numbers = list(numbers)

        else:
            size = random.randrange(1, 10)
            self.numbers = random.sample(range(1, 100), size)

    def correct_answer(self):
        return super().correct_answer()


# Ask the maximum number from a list of numbers
class MaximumQuestion(SelectFromListOfNumbersQuestion):
    def __init__(self, *numbers):
        super().__init__(*numbers)
        self.points = 40

    def as_text(self):
        return f"Which of the following numbers is the largest: {', '.join(map(str, self.numbers))}?"

    def correct_answer(self):
        return max(self.numbers)


# Ask the result of addition of 2 numbers
class AdditionQuestion(BinaryMathsQuestion):
    def as_text(self):
        return f"What is {self.n1} plus {self.n2}?"

    def correct_answer(self):
        return self.n1 + self.n2


# Ask the result of subtraction of 2 numbers
class SubtractionQuestion(BinaryMathsQuestion):
    def as_text(self):
        return f"What is {self.n1} minus {self.n2}?"

    def correct_answer(self):
        return self.n1 - self.n2


# Ask the result of multiplication of 2 numbers
class MultiplicationQuestion(BinaryMathsQuestion):
    def as_text(self):
        return f"What is {self.n1} multiplied by {self.n2}?"

    def correct_answer(self):
        return self.n1 * self.n2


# Ask the result of addition of 3 numbers
class AdditionAdditionQuestion(TernaryMathsQuestion):
    def __init__(self, *numbers):
        super().__init__(*numbers)
        self.points = 30

    def as_text(self):
        return f"What is {self.n1} plus {self.n2} plus {self.n3}?"

    def correct_answer(self):
        return self.n1 + self.n2 + self.n3


# Ask the result of addition followed by multiplication
class AdditionMultiplicationQuestion(TernaryMathsQuestion):
    def __init__(self, *numbers):
        super().__init__(*numbers)
        self.points = 60

    def as_text(self):
        return f"What is {self.n1} plus {self.n2} multiplied by {self.n3}"

    def correct_answer(self):
        return self.n1 + self.n2 * self.n3


# Ask the result of multiplication followed by addition
class MultiplicationAdditionQuestion(TernaryMathsQuestion):
    def __init__(self, *numbers):
        super().__init__(*numbers)
        self.points = 50

    def as_text(self):
        return f"What is {self.n1} multiplied by {self.n2} plus {self.n3}?"

    def correct_answer(self):
        return self.n1 * self.n2 + self.n3


# Ask the result of multiplication followed by addition
class PowerQuestion(BinaryMathsQuestion):
    def __init__(self, *numbers):
        super().__init__(*numbers)
        self.points = 50

    def as_text(self):
        return f"What is {self.n1} to the power of {self.n2}?"

    def correct_answer(self):
        return self.n1 ** self.n2


# Ask which number from list if numbers is a square number and a cube number
class SquareCubeQuestion(SelectFromListOfNumbersQuestion):
    def __init__(self, *numbers):
        super().__init__(*numbers)
        self.points = 50

    def as_text(self):
        return f"Which of the following numbers is both a square and a cube: {', '.join(map(str, self.numbers))}?"

    def correct_answer(self):
        is_square_cube = (
            lambda x: round(x ** (1 / 3)) ** 3 == x and round(x ** (1 / 3)) ** 3 == x
        )
        return ", ".join(map(str, filter(is_square_cube, self.numbers)))


# Ask which number from list if numbers is a prime number
class PrimesQuestion(SelectFromListOfNumbersQuestion):
    def __init__(self, *numbers):
        super().__init__(*numbers)
        self.points = 60

    def as_text(self):
        return f"Which of the following numbers are primes: {', '.join(map(str, self.numbers))}?"

    def correct_answer(self):
        is_prime = (
            lambda x: all([(x % j) for j in range(2, int(x ** 0.5) + 1)]) and x > 1
        )
        return ", ".join(map(str, filter(is_prime, self.numbers)))


# Ask the n-th Fibonacci number
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
        return f"What is the {str(self.number) + self.ordinal(11)} number in the Fibonacci sequence?"

    def fib(n):
        a, b = 0, 1
        for i in range(n):
            a, b = b, a + b

        return a

    def correct_answer(self):
        return FibonacciQuestion.fib(self.number)


# Ask a general knowledge questions from a file
class GeneralKnowledgeQuestion(Question):
    def __init__(self, question="", answer=""):
        super().__init__
        if question == "" or answer == "":
            with open("flaskr/yaml/general_knowledge.yaml", "r") as infile:
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


# Ask the anagram of a word given a list of correct and incorrect anagram
class AnagramQuestion(Question):
    def __init__(self, anagram="", correct="", incorrect=[]):
        super().__init__
        if anagram == "" or correct == "" or len(incorrect) == 0:
            with open("flaskr/yaml/anagrams.yaml", "r") as infile:
                anagrams = yaml.safe_load(infile)

            anagram = random.choice(anagrams)
            self.anagram, self.correct, self.incorrect = anagram.values()

        else:
            self.anagram, self.correct, self.incorrect = anagram, correct, incorrect

    def as_text(self):
        possible_words = [self.correct] + self.incorrect
        return f"Which of the following is an anagram of {anagram}: {', '.join(random.shuffle(possible_words))}?"

    def correct_answer(self):
        return self.correct


# Ask the scrabble score of a word
class ScrabbleQuestion(Question):
    SCRABBLE_SCORES = {
        "a": 1,
        "c": 3,
        "b": 3,
        "e": 1,
        "d": 2,
        "g": 2,
        "f": 4,
        "i": 1,
        "h": 4,
        "k": 5,
        "j": 8,
        "m": 3,
        "l": 1,
        "o": 1,
        "n": 1,
        "q": 10,
        "p": 3,
        "s": 1,
        "r": 1,
        "u": 1,
        "t": 1,
        "w": 4,
        "v": 4,
        "y": 4,
        "x": 8,
        "z": 10,
    }

    def __init__(self, word=""):
        super().__init__()
        if word == "":
            self.word = random.choice(
                ["banana", "september", "cloud", "zoo", "ruby", "buzzword"]
            )

        else:
            self.word = word.lower()

    def as_text(self):
        return f"What is the scrabble score of {self.word}?"

    def score(word):
        score = 0
        for c in word:
            score += ScrabbleQuestion.SCRABBLE_SCORES[c]

        return score

    def correct_answer(self):
        return ScrabbleQuestion.score(self.word)


# utilities function to check constructor argument is valid and have the correct lenght
def valid_num_arguments(arg_num, numbers):
    return len(list(numbers)) == arg_num and all(
        isinstance(num, int) for num in numbers
    )
