from flaskr.question_factory import QuestionFactory
from flaskr.questions import WarmupQuestion, Question
import pytest
from unittest.mock import Mock, patch


@pytest.fixture
def setup_question_factory_with_round(round):
    pass
    # def generate_question(number):
    #     question = Question()
    #     mocker.patch("flaskr.questions.Question.as_text", return_value=f"this is question {number}")

    # def _setup():
    #     factory = QuestionFactory(round)
    #     factory.question_types =


def test_default_initialised_properly():
    factory = QuestionFactory()
    assert factory.round == 1
    assert len(factory.question_types) != 0
    assert factory.question_types[0] is WarmupQuestion
    assert all([issubclass(q, Question) for q in factory.question_types])


def test_can_advance_round():
    factory = QuestionFactory(0)
    assert factory.round == 0
    factory.advance_round()
    assert factory.round == 1
    factory.advance_round()
    assert factory.round == 2


def test_zero_round_asks_warmup_question_only():
    factory = QuestionFactory(0)
    for _ in range(5):
        assert factory.next_question().as_text() == "What is your name?"


def test_1st_round_asks_1st_question_only():
    pass


def test_2st_round_asks_1st_2nd_question_only():
    pass


def test_3st_round_asks_1st_to_4rd_question_only():
    pass


def test_4st_round_asks_3st_to__6rd_question_only():
    pass


def test_5st_round_asks_5th_to__8th_question_only():
    pass


def test_5st_round_asks_5th_to__8th_question_only():
    pass
