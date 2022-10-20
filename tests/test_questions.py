from flaskr.questions import *


def test_addition_question():
    sub_question = SubtractionQuestion(50, 31)
    assert sub_question.as_text() == "What is 50 minus 31"
    assert sub_question.points == 10
    assert sub_question.correct_answer() == 19


def test_addition_question_random():
    sub_question = SubtractionQuestion()
    n1, n2 = sub_question.n1, sub_question.n2
    assert sub_question.as_text() == f"What is {n1} minus {n2}"
    assert sub_question.points == 10
    assert sub_question.correct_answer() == n1 - n2


def test_addition_addition_question_random():
    sub_question = AdditionAdditionQuestion()
    n1, n2, n3 = sub_question.n1, sub_question.n2, sub_question.n3
    assert sub_question.as_text() == f"What is {n1} plus {n2} plus {n3}"
    assert sub_question.points == 30
    assert sub_question.correct_answer() == n1 + n2 + n3


def test_addition_addition_question():
    sub_question = AdditionAdditionQuestion(10, 20, 30)
    n1, n2, n3 = sub_question.n1, sub_question.n2, sub_question.n3
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
