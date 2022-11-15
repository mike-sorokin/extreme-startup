import sys

sys.path.append(".")

from flaskr.game import Game
from unittest.mock import Mock
import pytest

PASSWORD = "dummy_password"
DUMMY_ID = "1234"
ARBITRARY_RESPONSE_SEQ = "1X01X01X01X0"


@pytest.fixture()
def basic_game():
    return Game(PASSWORD)


@pytest.fixture()
def basic_game_with_five_players():
    game, players = Game(PASSWORD), [Mock() for _ in range(5)]
    game.pause()

    for i, player in enumerate(players):
        player.uuid = DUMMY_ID + str(i)
        player.streak = ""
        player.round_index = 0
        game.add_player(player)

    players[0].streak = ARBITRARY_RESPONSE_SEQ + "0X" * 8
    players[1].streak = ARBITRARY_RESPONSE_SEQ + "1" + "X" * 16
    players[2].streak = ARBITRARY_RESPONSE_SEQ + "1" + "0" * 16
    players[3].streak = ARBITRARY_RESPONSE_SEQ + "1" + "X" * 15
    players[4].streak = ARBITRARY_RESPONSE_SEQ + "1" + "0" * 15

    for i in range(len(players)):
        players[i].round_index = len(players[i].streak)

    return game, players


def test_game_initialises_with_no_players(basic_game):
    assert len(basic_game.players) == 0


def test_game_defaults_to_round_zero(basic_game):
    assert basic_game.round == 0


def test_game_defaults_to_not_paused(basic_game):
    assert basic_game.running.is_set()


def test_game_defaults_to_no_assists(basic_game):
    assert len(basic_game.players_to_assist) == 0


def test_game_defaults_to_manual_mode(basic_game):
    assert basic_game.auto_mode == False


def test_game_can_append_new_players(basic_game):
    player1 = Mock()
    player1.uuid = "dummy_id_1"
    player1.streak = ""
    player1.round_index = 0
    basic_game.add_player(player1)
    assert len(basic_game.players) == 1
    assert player1.uuid in basic_game.players

    player2 = Mock()
    player2.uuid = "dummy_id_2"
    player2.streak = ""
    player2.round_index = 0
    basic_game.add_player(player2)
    assert len(basic_game.players) == 2
    assert player2.uuid in basic_game.players


def test_players_with_more_than_fifteen_incorect_gets_added_to_assistance_list(
    basic_game_with_five_players,
):
    game, players = basic_game_with_five_players
    game._Game__update_players_to_assist()

    assert players[0].uuid in game.players_to_assist
    assert players[1].uuid in game.players_to_assist
    assert players[2].uuid in game.players_to_assist
    assert len(game.players_to_assist) == 3


def test_player_who_gets_one_correct_after_requiring_assistance_no_longer_needs_help(
    basic_game_with_five_players,
):
    game, players = basic_game_with_five_players
    game._Game__update_players_to_assist()

    game.players[players[0].uuid].streak += "1"
    game.players[players[0].uuid].round_index += 1

    game._Game__update_players_to_assist()

    assert players[0].uuid not in game.players_to_assist
    assert players[1].uuid in game.players_to_assist
    assert players[2].uuid in game.players_to_assist
    assert len(game.players_to_assist) == 2


# TODO: Tets auto_increment_round
