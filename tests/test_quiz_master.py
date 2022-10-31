import sys

sys.path.append(".")

from flaskr.quiz_master import QuizMaster
from unittest.mock import Mock


def test_quiz_master_sends_questions_while_player_active():
    player, rc, question_factory, scoreboard, lock, e = (
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )

    quiz_master = QuizMaster(player, question_factory, scoreboard, lock, rc)
    lock.acquire.return_value = True
    lock.release.return_value = True

    quiz_master.administer_question(e)

    # assertion(s)
    scoreboard.record_request_for.assert_called()
    scoreboard.increment_score_for.assert_called()
    lock.acquire.assert_called()
    lock.release.assert_called()
    rc.wait_for_next_request.assert_called()
    rc.update_algorithm_based_on_score.assert_called()
