from flaskr.questions import *


def test_addition_question():
    sub_question = SubtractionQuestion(50, 31)
    assert sub_question.as_text() == "What is 50 minus 31"
    assert sub_question.points == 10
    assert sub_question.correct_answer() == 19


def test_addition_question_random():
    sub_question = SubtractionQuestion()
    n1, n2 = sub_question.n1, sub_question.n2
    assert n1 != 0 or n2 != 0
    assert sub_question.as_text() == f"What is {n1} minus {n2}"
    assert sub_question.points == 10
    assert sub_question.correct_answer() == n1 - n2


def test_addition_addition_question_random():
    sub_question = AdditionAdditionQuestion()
    n1, n2, n3 = sub_question.n1, sub_question.n2, sub_question.n3
    assert n1 != 0 or n2 != 0 or n3 != 0
    assert sub_question.as_text() == f"What is {n1} plus {n2} plus {n3}"
    assert sub_question.points == 30
    assert sub_question.correct_answer() == n1 + n2 + n3


def test_addition_addition_question():
    sub_question = AdditionAdditionQuestion(10, 20, 30)
    assert sub_question.as_text() == "What is 10 plus 20 plus 30"
    assert sub_question.points == 30
    assert sub_question.correct_answer() == 60


def test_maximum_question():
    max_question = MaximumQuestion(1, 2, 3, 4, 5)
    assert (
        max_question.as_text()
        == "which of the following numbers is the largest: 1, 2, 3, 4, 5"
    )
    assert max_question.points == 40
    assert max_question.correct_answer() == 5


def test_maximum_question_random():
    max_question = MaximumQuestion()
    numbers = max_question.numbers
    assert len(numbers) != 0
    assert (
        max_question.as_text()
        == f"which of the following numbers is the largest: {', '.join(map(str, numbers))}"
    )
    assert max_question.points == 40
    assert max_question.correct_answer() == max(numbers)


def test_square_cube_question():
    square_cube_question = SquareCubeQuestion(2, 64, 100)
    assert (
        square_cube_question.as_text()
        == "which of the following numbers is both a square and a cube: 2, 64, 100"
    )
    assert square_cube_question.points == 50
    assert square_cube_question.correct_answer() == "64"


def test_square_cube_question_multiple():
    square_cube_question = SquareCubeQuestion(0, 1, 64, 100)
    assert (
        square_cube_question.as_text()
        == "which of the following numbers is both a square and a cube: 0, 1, 64, 100"
    )
    assert square_cube_question.points == 50
    assert square_cube_question.correct_answer() == "0, 1, 64"


def test_square_cube_question_no_ans():
    square_cube_question = SquareCubeQuestion(2, 65, 101)
    assert (
        square_cube_question.as_text()
        == "which of the following numbers is both a square and a cube: 2, 65, 101"
    )
    assert square_cube_question.points == 50
    assert square_cube_question.correct_answer() == ""


def test_square_cube_question_random():
    square_cube_question = SquareCubeQuestion()
    numbers = square_cube_question.numbers
    is_square_cube = (
        lambda x: round(x ** (1 / 3)) ** 3 == x and round(x ** (1 / 3)) ** 3 == x
    )
    assert (
        square_cube_question.as_text()
        == f"which of the following numbers is both a square and a cube: {', '.join(map(str, numbers))}"
    )
    assert square_cube_question.points == 50
    assert square_cube_question.correct_answer() == ", ".join(
        map(str, filter(is_square_cube, numbers))
    )


def test_prime_question():
    prime_question = PrimesQuestion(2, 4, 7, 9)
    assert (
        prime_question.as_text()
        == "which of the following numbers are primes: 2, 4, 7, 9"
    )
    assert prime_question.points == 60
    assert prime_question.correct_answer() == "2, 7"


def test_prime_question():
    fib_question = FibonacciQuestion(11)
    assert fib_question.as_text() == "what is the 11th number in the Fibonacci sequence"
    assert fib_question.points == 50
    assert fib_question.correct_answer() == 89


def test_prime_question_random():
    fib_question = FibonacciQuestion()
    number = fib_question.number
    assert number != 0
    assert fib_question.points == 50
