import sys

sys.path.append(".")

from flaskr.scoreboard import Scoreboard
from unittest.mock import Mock, MagicMock
import pytest

PROBLEM_DECREMENT = 50


@pytest.fixture()
def game_setup():  # (scoreboard, player, question)
    return (Scoreboard(), MagicMock())


@pytest.fixture()
def game_with_player_setup():
    sb, player = Scoreboard(), MagicMock()
    sb.new_player(player)
    return (sb, player)


@pytest.fixture()
def full_game_setup():
    sb, player, question = Scoreboard(), MagicMock(), Mock()
    sb.new_player(player)
    yield (sb, player, question)
    del sb


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


def test_can_increment_score_for_player_with_correct_result(full_game_setup):
    scoreboard, player, question = full_game_setup
    points = 10
    question.result, question.points = "CORRECT", points
    scoreboard.increment_score_for(player, question)

    assert scoreboard.scores[player.uuid] == points
    assert scoreboard.correct_tally[player.uuid] == 1
    player.log_event.assert_called_once()


def test_can_decrement_score_for_player_with_incorrect_result(full_game_setup):
    scoreboard, player, question = full_game_setup
    points = 10
    question.result, question.points = "WRONG", points
    scoreboard.increment_score_for(player, question)

    assert scoreboard.scores[player.uuid] == -1 * points
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


def test_leaderboard_orders_players_by_decreasing_socre(full_game_setup):
    scoreboard, player1, question = full_game_setup
    player2 = MagicMock()
    scoreboard.new_player(player2)
    question.result, question.points = "CORRECT", 10

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
    worse_player, points = MagicMock(), 10
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

# Test Delay 