import sys

sys.path.append(".")

from flaskr.shared.questions import *
import pytest

UNARY_MATH_QUESTIONS = [FibonacciQuestion]
BINARY_MATH_QUESTIONS = [AdditionQuestion, SubtractionQuestion, MultiplicationQuestion]
TERNARY_MATH_QUESTIONS = [
    AdditionAdditionQuestion,
    AdditionMultiplicationQuestion,
    MultiplicationAdditionQuestion,
]
SELECT_NUMBERS_QUESTIONS = [MaximumQuestion, SquareCubeQuestion, PrimesQuestion]


@pytest.mark.parametrize("q", UNARY_MATH_QUESTIONS)
def test_unary_math_question(q):
    question = q(23)
    assert question.number == 23


@pytest.mark.parametrize("q", UNARY_MATH_QUESTIONS)
def test_unary_math_question_random(q):
    question = q()
    assert type(question.number) is int
    assert question.number in range(1, 100)


@pytest.mark.parametrize("q", BINARY_MATH_QUESTIONS)
def test_binary_math_question(q):
    question = q(23, 47)
    assert question.n1 == 23
    assert question.n2 == 47


@pytest.mark.parametrize("q", BINARY_MATH_QUESTIONS)
def test_binary_math_question_random(q):
    question = q()
    assert type(question.n1) is int
    assert type(question.n2) is int
    assert question.n1 in range(1, 100)
    assert question.n2 in range(1, 100)


@pytest.mark.parametrize("q", TERNARY_MATH_QUESTIONS)
def test_ternary_math_question(q):
    question = q(25, 47, 49)
    assert question.n1 == 25
    assert question.n2 == 47
    assert question.n3 == 49


@pytest.mark.parametrize("q", TERNARY_MATH_QUESTIONS)
def test_ternary_math_question_random(q):
    question = q()
    assert type(question.n1) is int
    assert type(question.n2) is int
    assert type(question.n3) is int
    assert question.n1 in range(1, 100)
    assert question.n2 in range(1, 100)
    assert question.n3 in range(1, 100)


@pytest.mark.parametrize("q", SELECT_NUMBERS_QUESTIONS)
def test_select_numbers_question(q):
    question = q(25, 47, 49, 58)
    assert question.numbers == [25, 47, 49, 58]


@pytest.mark.parametrize("q", SELECT_NUMBERS_QUESTIONS)
def test_select_numbers_question_random(q):
    question = q()
    assert type(question.numbers) is list
    assert len(question.numbers) in range(1, 10)
    assert all([1 <= i < 100 for i in question.numbers])


def test_fibonacci_question():
    fib_question = FibonacciQuestion(11)
    assert (
        fib_question.as_text() == "What is the 11th number in the Fibonacci sequence?"
    )
    assert fib_question.points == 50
    assert fib_question.correct_answer() == 89


def test_addition_question():
    add_question = AdditionQuestion(50, 31)
    assert add_question.as_text() == "What is 50 plus 31?"
    assert add_question.points == 10
    assert add_question.correct_answer() == 50 + 31


def test_subtraction_question():
    sub_question = SubtractionQuestion(50, 31)
    assert sub_question.as_text() == "What is 50 minus 31?"
    assert sub_question.points == 10
    assert sub_question.correct_answer() == 50 - 31


def test_multiplication_question():
    mul_question = MultiplicationQuestion(50, 4)
    assert mul_question.as_text() == "What is 50 multiplied by 4?"
    assert mul_question.points == 10
    assert mul_question.correct_answer() == 50 * 4


def test_addition_addition_question():
    sub_question = AdditionAdditionQuestion(10, 20, 30)
    assert sub_question.as_text() == "What is 10 plus 20 plus 30?"
    assert sub_question.points == 30
    assert sub_question.correct_answer() == 10 + 20 + 30


def test_addition_multiplication_question():
    add_mul_question = AdditionMultiplicationQuestion(10, 20, 30)
    assert add_mul_question.as_text() == "What is 10 plus 20 multiplied by 30?"
    assert add_mul_question.points == 60
    assert add_mul_question.correct_answer() == 10 + 20 * 30


def test_addition_multiplication_question():
    mul_add_question = MultiplicationAdditionQuestion(10, 20, 30)
    assert mul_add_question.as_text() == "What is 10 multiplied by 20 plus 30?"
    assert mul_add_question.points == 50
    assert mul_add_question.correct_answer() == 10 * 20 + 30


def test_maximum_question():
    max_question = MaximumQuestion(1, 2, 3, 4, 5)
    assert (
        max_question.as_text()
        == "Which of the following numbers is the largest: 1, 2, 3, 4, 5?"
    )
    assert max_question.points == 40
    assert max_question.correct_answer() == 5


def test_square_cube_question():
    square_cube_question = SquareCubeQuestion(2, 64, 100)
    assert (
        square_cube_question.as_text()
        == "Which of the following numbers is both a square and a cube: 2, 64, 100?"
    )
    assert square_cube_question.points == 50
    assert square_cube_question.correct_answer() == "64"


def test_square_cube_question_multiple():
    square_cube_question = SquareCubeQuestion(0, 1, 64, 100)
    assert (
        square_cube_question.as_text()
        == "Which of the following numbers is both a square and a cube: 0, 1, 64, 100?"
    )
    assert square_cube_question.points == 50
    assert square_cube_question.correct_answer() == "0, 1, 64"


def test_square_cube_question_no_ans():
    square_cube_question = SquareCubeQuestion(2, 65, 101)
    assert (
        square_cube_question.as_text()
        == "Which of the following numbers is both a square and a cube: 2, 65, 101?"
    )
    assert square_cube_question.points == 50
    assert square_cube_question.correct_answer() == ""


def test_prime_question():
    prime_question = PrimesQuestion(2, 4, 9)
    assert (
        prime_question.as_text()
        == "Which of the following numbers are primes: 2, 4, 9?"
    )
    assert prime_question.points == 60
    assert prime_question.correct_answer() == "2"


def test_prime_question_multiple():
    prime_question = PrimesQuestion(2, 4, 7, 9)
    assert (
        prime_question.as_text()
        == "Which of the following numbers are primes: 2, 4, 7, 9?"
    )
    assert prime_question.points == 60
    assert prime_question.correct_answer() == "2, 7"


def test_prime_question_no_ans():
    prime_question = PrimesQuestion(1, 6, 8, 9)
    assert (
        prime_question.as_text()
        == "Which of the following numbers are primes: 1, 6, 8, 9?"
    )
    assert prime_question.points == 60
    assert prime_question.correct_answer() == ""


def test_scrabble_question_random_initialised():
    scrabble_question = ScrabbleQuestion()
    assert scrabble_question.word in [
        "banana",
        "september",
        "cloud",
        "zoo",
        "ruby",
        "buzzword",
    ]


def test_scrabble_question():
    scrabble_question = ScrabbleQuestion("Helix")
    assert scrabble_question.word == "helix"
    assert scrabble_question.as_text() == "What is the scrabble score of helix?"
    assert scrabble_question.points == 10
    assert scrabble_question.correct_answer() == 4 + 1 + 1 + 1 + 8


def test_general_knowledge_question_random_initialised():
    general_question = GeneralKnowledgeQuestion()
    with open("flaskr/yaml/general_knowledge.yaml", "r") as infile:
        ques_ans_list = yaml.safe_load(infile)
    assert general_question.question in map(lambda i: i["question"], ques_ans_list)
    assert general_question.answer in map(lambda i: i["answer"], ques_ans_list)
    assert (
        general_question.correct_answer()
        == list(
            filter(lambda i: i["question"] == general_question.question, ques_ans_list)
        )[0]["answer"]
    )


def test_general_knowledge_question():
    general_question = GeneralKnowledgeQuestion(
        "Who was the shortest-serving prime minister in the UK?", "lizz truss"
    )
    assert (
        general_question.question
        == "Who was the shortest-serving prime minister in the UK?"
    )
    assert general_question.answer == "lizz truss"
    assert general_question.correct_answer() == "lizz truss"


def test_anagram_question_random_initialised():
    anagram_question = AnagramQuestion()
    with open("flaskr/yaml/anagrams.yaml", "r") as infile:
        anagrams = yaml.safe_load(infile)
    assert anagram_question.anagram in map(lambda i: i["anagram"], anagrams)
    assert anagram_question.correct in map(lambda i: i["correct"], anagrams)
    assert anagram_question.incorrect in map(lambda i: i["incorrect"], anagrams)
    assert (
        anagram_question.correct_answer()
        == list(
            filter(
                lambda i: i["anagram"] == anagram_question.anagram
                and i["correct"] == anagram_question.correct,
                anagrams,
            )
        )[0]["correct"]
    )


def test_anagram_question():
    anagram_question = AnagramQuestion(
        "a decimal point", "im a dot in place", ["random question", "not an anagram"]
    )
    assert anagram_question.anagram == "a decimal point"
    assert anagram_question.correct == "im a dot in place"
    assert anagram_question.incorrect == ["random question", "not an anagram"]
    assert anagram_question.correct_answer() == "im a dot in place"
