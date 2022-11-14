import sys

sys.path.append(".")

from flaskr.quiz_master import QuizMaster
from unittest.mock import Mock
import pytest


@pytest.fixture()
def basic_quiz_master():
    player, rc, question_factory, scoreboard, warmup_over, running = (
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock()
    )

    yield (
        QuizMaster(player, question_factory, scoreboard, rc),
        player,
        rc,
        question_factory,
        scoreboard,
        warmup_over,
        running,
    )


def test_quiz_master_sends_questions_while_player_active(basic_quiz_master):
    quiz_master, _, rc, _, scoreboard, warmup_over, running = basic_quiz_master

    quiz_master.administer_question(warmup_over, running)

    # assertion(s)
    scoreboard.record_request_for.assert_called()
    scoreboard.increment_score_for.assert_called()
    running.wait.assert_called()
    rc.wait_for_next_request.assert_called()
    rc.update_algorithm_based_on_score.assert_called()


def test_reset_player_changes_streak_to_empty_str_and_resets_score_and_rc(
    basic_quiz_master,
):
    quiz_master, player, rc, _, scoreboard, _, _ = basic_quiz_master
    player.streak = "X"
    player.round_index = 1  # any non-zero value

    quiz_master.reset_stats_and_rc()

    assert player.streak == ""
    assert player.round_index == 0
    scoreboard.reset_player.assert_called()
    rc.reset.assert_called()
