import sys

sys.path.append(".")

from flaskr.scoreboard import Scoreboard
from unittest.mock import Mock
import pytest

PROBLEM_DECREMENT = 50
DEFAULT_POINT_SCORE = 10


@pytest.fixture()
def game_setup():  # (scoreboard, question)
    return (Scoreboard(), Mock())


@pytest.fixture()
def game_with_player_setup():
    sb, player = Scoreboard(), Mock()

    player.longest_streak = player.curr_streak_length = 0
    player.round_index = 0
    player.streak = ""

    sb.new_player(player)
    yield (sb, player)
    del sb, player


@pytest.fixture()
def full_game_setup():
    sb, player, question = Scoreboard(), Mock(), Mock()
    player.longest_streak = player.curr_streak_length = 0
    player.streak = ""
    player.round_index = 0

    sb.new_player(player)
    yield (sb, player, question)
    del sb, player, question


def test_scoreboard_can_add_new_player(game_setup):
    scoreboard, player = game_setup

    assert len(scoreboard.scores) == 0
    scoreboard.new_player(player)

    # insertion assertions
    assert len(scoreboard.scores) == 1
    assert len(scoreboard.request_counts) == 1
    assert len(scoreboard.correct_tally) == 1
    assert len(scoreboard.incorrect_tally) == 1

    assert scoreboard.scores[player.uuid] == 0
    assert scoreboard.request_counts[player.uuid] == 0
    assert scoreboard.correct_tally[player.uuid] == 0
    assert scoreboard.incorrect_tally[player.uuid] == 0


def test_scoreboard_can_delete_player(game_with_player_setup):
    scoreboard, player = game_with_player_setup
    scoreboard.delete_player(player)

    # deletion assertions
    assert len(scoreboard.scores) == 0
    assert len(scoreboard.request_counts) == 0
    assert len(scoreboard.correct_tally) == 0
    assert len(scoreboard.incorrect_tally) == 0


def test_scoreboard_can_have_multiple_players(game_setup):
    scoreboard, _ = game_setup
    num_players = 10
    for i in range(num_players):
        scoreboard.new_player(Mock())

    # multiple insertion assertions
    assert len(scoreboard.scores) == num_players
    assert len(scoreboard.request_counts) == num_players
    assert len(scoreboard.correct_tally) == num_players
    assert len(scoreboard.incorrect_tally) == num_players


def test_scoring_increases_round_index(full_game_setup):
    scoreboard, player, question = full_game_setup
    question.result, question.points = "CORRECT", DEFAULT_POINT_SCORE

    scoreboard.increment_score_for(player, question)
    assert player.round_index == 1


def test_can_increment_score_for_player_with_correct_result(full_game_setup):
    scoreboard, player, question = full_game_setup
    question.result, question.points = "CORRECT", DEFAULT_POINT_SCORE

    scoreboard.increment_score_for(player, question)

    assert scoreboard.scores[player.uuid] == DEFAULT_POINT_SCORE
    assert scoreboard.correct_tally[player.uuid] == 1
    player.log_event.assert_called_once()


def test_can_decrement_score_for_player_with_incorrect_result(full_game_setup):
    scoreboard, player, question = full_game_setup
    question.result, question.points = "WRONG", DEFAULT_POINT_SCORE

    scoreboard.increment_score_for(player, question)

    assert scoreboard.scores[player.uuid] == -1 * DEFAULT_POINT_SCORE
    assert scoreboard.incorrect_tally[player.uuid] == 1
    player.log_event.assert_called_once()


def test_decrements_score_for_question_with_error_response(full_game_setup):
    scoreboard, player, question = full_game_setup
    question.problem = "ERROR_RESPONSE"

    scoreboard.increment_score_for(player, question)

    assert scoreboard.scores[player.uuid] == -1 * PROBLEM_DECREMENT
    assert scoreboard.incorrect_tally[player.uuid] == 1

    question.problem = "NO_SERVER_RESPONSE"
    scoreboard.increment_score_for(player, question)

    assert scoreboard.scores[player.uuid] == -2 * PROBLEM_DECREMENT
    assert scoreboard.incorrect_tally[player.uuid] == 2


def test_leaderboard_orders_players_by_decreasing_score(full_game_setup):
    scoreboard, player1, question = full_game_setup
    player2 = Mock()
    player2.streak = ""
    player2.curr_streak_length = player2.longest_streak = player2.round_index = 0
    
    scoreboard.new_player(player2)
    question.result, question.points = "CORRECT", DEFAULT_POINT_SCORE

    scoreboard.increment_score_for(player1, question)
    scoreboard.increment_score_for(player1, question)

    assert scoreboard.leaderboard_position(player1) == 1
    assert scoreboard.leaderboard_position(player2) == 2

    scoreboard.increment_score_for(player2, question)
    scoreboard.increment_score_for(player2, question)
    scoreboard.increment_score_for(player2, question)

    assert scoreboard.leaderboard_position(player2) == 1
    assert scoreboard.leaderboard_position(player1) == 2


def test_scoreboard_penalises_higher_ranking_players_more(full_game_setup):
    scoreboard, better_player, question = full_game_setup
    worse_player, points = Mock(), DEFAULT_POINT_SCORE
    worse_player.streak = ""
    worse_player.round_index = 0
    num_players = 2
    scoreboard.new_player(worse_player)
    question.result, question.points = "CORRECT", points

    # better_player gets out in front of worse_player
    scoreboard.increment_score_for(better_player, question)
    question.result = "WRONG"
    scoreboard.increment_score_for(worse_player, question)
    diff_for_worse_player = scoreboard.scores[worse_player.uuid]
    scoreboard.increment_score_for(better_player, question)
    diff_for_better_player = scoreboard.scores[better_player.uuid] - points

    assert diff_for_worse_player == -1 * float(points) / num_players
    assert diff_for_better_player == -1 * float(points)
    assert diff_for_better_player < diff_for_worse_player


def test_reseting_player_sets_score_and_tally_and_request_count_to_zero(
    full_game_setup,
):
    scoreboard, player, question = full_game_setup
    scoreboard.new_player(player)
    question.result, question.problem, question.points = (
        "CORRECT",
        "",
        DEFAULT_POINT_SCORE,
    )

    scoreboard.increment_score_for(player, question)
    scoreboard.record_request_for(player)
    assert scoreboard.scores[player.uuid] == 10
    assert scoreboard.correct_tally[player.uuid] == 1
    assert scoreboard.incorrect_tally[player.uuid] == 0
    assert scoreboard.request_counts[player.uuid] == 1
    assert player.score == 10

    scoreboard.reset_player(player)

    assert scoreboard.correct_tally[player.uuid] == 0
    assert scoreboard.request_counts[player.uuid] == 0

    assert scoreboard.scores[player.uuid] == 0
    assert player.score == 0
