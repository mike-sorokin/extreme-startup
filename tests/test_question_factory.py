import sys

sys.path.append(".")

from flaskr.shared.question_factory import QuestionFactory, MAX_ROUND
from flaskr.shared.questions import WarmupQuestion, Question
import pytest
import random
from unittest.mock import Mock, patch


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


def test_1st_round_asks_1st_2nd_question_only():
    first_round = QuestionFactory(1)
    assert first_round.window_end == 2
    assert first_round.window_start == 0


def test_2st_round_asks_1st_to_4th_question_only():
    second_round = QuestionFactory(2)
    assert second_round.window_end == 4
    assert second_round.window_start == 0


def test_n_plus_first_round_shifts_nth_round_window_by_two():
    n = random.randint(2, MAX_ROUND - 1)
    nth_factory = QuestionFactory(n)

    n_window_start = nth_factory.window_start
    n_window_end = nth_factory.window_end

    nth_factory.advance_round()
    assert nth_factory.window_start - n_window_start == 2
    assert nth_factory.window_end - n_window_end == 2
