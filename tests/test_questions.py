from flaskr.questions import *

UNARY_MATH_QUESTIONS = [FibonacciQuestion]
BINARY_MATH_QUESTIONS = [AdditionQuestion, SubtractionQuestion, MultiplicationQuestion]
TERNRARY_MATH_QUESTIONS = [
    AdditionAdditionQuestion,
    AdditionMultiplicationQuestion,
    MultiplicationAdditionQuestion,
]
SELECT_NUMBERS_QUESTIONS = [MaximumQuestion, SquareCubeQuestion, PrimesQuestion]


def test_unary_math_question():
    unary_questions = [q(23) for q in UNARY_MATH_QUESTIONS]
    for question in unary_questions:
        assert question.number == 23


def test_unary_math_question_random():
    unary_questions = [q() for q in UNARY_MATH_QUESTIONS]
    for question in unary_questions:
        assert type(question.number) is int
        assert question.number in range(1, 100)


def test_binary_math_question():
    bin_questions = [q(23, 47) for q in BINARY_MATH_QUESTIONS]
    for question in bin_questions:
        assert question.n1 == 23
        assert question.n2 == 47


def test_binary_math_question_random():
    bin_questions = [q() for q in BINARY_MATH_QUESTIONS]
    for question in bin_questions:
        assert type(question.n1) is int
        assert type(question.n2) is int
        assert question.n1 in range(1, 100)
        assert question.n2 in range(1, 100)


def test_ternary_math_question():
    ter_questions = [q(25, 47, 49) for q in TERNRARY_MATH_QUESTIONS]
    for question in ter_questions:
        assert question.n1 == 25
        assert question.n2 == 47
        assert question.n3 == 49


def test_ternary_math_question_random():
    ter_questions = [q() for q in TERNRARY_MATH_QUESTIONS]
    for question in ter_questions:
        assert type(question.n1) is int
        assert type(question.n2) is int
        assert type(question.n3) is int
        assert question.n1 in range(1, 100)
        assert question.n2 in range(1, 100)
        assert question.n3 in range(1, 100)


def test_fibonacci_question():
    fib_question = FibonacciQuestion(11)
    assert fib_question.as_text() == "what is the 11th number in the Fibonacci sequence"
    assert fib_question.points == 50
    assert fib_question.correct_answer() == 89


def test_addition_question():
    add_question = AdditionQuestion(50, 31)
    assert add_question.as_text() == "What is 50 plus 31"
    assert add_question.points == 10
    assert add_question.correct_answer() == 50 + 31


def test_subtraction_question():
    sub_question = SubtractionQuestion(50, 31)
    assert sub_question.as_text() == "What is 50 minus 31"
    assert sub_question.points == 10
    assert sub_question.correct_answer() == 50 - 31


def test_multiplication_question():
    mul_question = MultiplicationQuestion(50, 4)
    assert mul_question.as_text() == "What is 50 multiplied by 4"
    assert mul_question.points == 10
    assert mul_question.correct_answer() == 50 * 4


def test_addition_addition_question():
    sub_question = AdditionAdditionQuestion(10, 20, 30)
    assert sub_question.as_text() == "What is 10 plus 20 plus 30"
    assert sub_question.points == 30
    assert sub_question.correct_answer() == 10 + 20 + 30


def test_addition_multiplication_question():
    add_mul_question = AdditionMultiplicationQuestion(10, 20, 30)
    assert add_mul_question.as_text() == "What is 10 plus 20 multiplied by 30"
    assert add_mul_question.points == 60
    assert add_mul_question.correct_answer() == 10 + 20 * 30


def test_addition_multiplication_question():
    mul_add_question = MultiplicationAdditionQuestion(10, 20, 30)
    assert mul_add_question.as_text() == "What is 10 multiplied by 20 plus 30"
    assert mul_add_question.points == 50
    assert mul_add_question.correct_answer() == 10 * 20 + 30


def test_maximum_question():
    max_question = MaximumQuestion(1, 2, 3, 4, 5)
    assert (
        max_question.as_text()
        == "which of the following numbers is the largest: 1, 2, 3, 4, 5"
    )
    assert max_question.points == 40
    assert max_question.correct_answer() == 5


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


def test_prime_question():
    prime_question = PrimesQuestion(2, 4, 9)
    assert (
        prime_question.as_text() == "which of the following numbers are primes: 2, 4, 9"
    )
    assert prime_question.points == 60
    assert prime_question.correct_answer() == "2"


def test_prime_question_multiple():
    prime_question = PrimesQuestion(2, 4, 7, 9)
    assert (
        prime_question.as_text()
        == "which of the following numbers are primes: 2, 4, 7, 9"
    )
    assert prime_question.points == 60
    assert prime_question.correct_answer() == "2, 7"


def test_prime_question_no_ans():
    prime_question = PrimesQuestion(1, 6, 8, 9)
    assert (
        prime_question.as_text()
        == "which of the following numbers are primes: 1, 6, 8, 9"
    )
    assert prime_question.points == 60
    assert prime_question.correct_answer() == ""


def test_prime_question_random():
    fib_question = FibonacciQuestion()
    number = fib_question.number
    assert number in range(0, 100)
    assert fib_question.points == 50
