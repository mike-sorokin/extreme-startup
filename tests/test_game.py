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
    players_dict = {}

    for i, player in enumerate(players):
        player.id = DUMMY_ID + str(i)
        game.new_player(player.id)
        players_dict[player.id] = player

    players[0].streak = ARBITRARY_RESPONSE_SEQ + "0X" * 8
    players[1].streak = ARBITRARY_RESPONSE_SEQ + "1" + "X" * 16
    players[2].streak = ARBITRARY_RESPONSE_SEQ + "1" + "0" * 16
    players[3].streak = ARBITRARY_RESPONSE_SEQ + "1" + "X" * 15
    players[4].streak = ARBITRARY_RESPONSE_SEQ + "1" + "0" * 15

    for i in range(len(players)):
        players[i].round_index = len(players[i].streak)

    return game, players, players_dict


def test_game_initialises_with_no_players(basic_game):
    assert len(basic_game.players) == 0


def test_game_defaults_to_round_zero(basic_game):
    assert basic_game.round == 0


def test_game_defaults_to_not_paused(basic_game):
    assert basic_game.paused == False


def test_game_defaults_to_no_assists(basic_game):
    assert len(basic_game.players_to_assist) == 0


def test_game_defaults_to_manual_mode(basic_game):
    assert basic_game.auto_mode == False


def test_game_can_append_new_players(basic_game):
    basic_game.new_player("dummy_id")
    assert len(basic_game.players) == 1
    assert "dummy_id" in basic_game.players

    basic_game.new_player("dummy_id_2")
    assert len(basic_game.players) == 2
    assert "dummy_id_2" in basic_game.players


def test_players_with_more_than_fifteen_incorect_gets_added_to_assistance_list(
    basic_game_with_five_players
):
    game, players, players_dict = basic_game_with_five_players
    game._Game__update_players_to_assist(players_dict)

    assert players[0].id in game.players_to_assist
    assert players[1].id in game.players_to_assist
    assert players[2].id in game.players_to_assist
    assert len(game.players_to_assist) == 3


def test_player_who_gets_one_correct_after_requiring_assistance_no_longer_needs_help(
    basic_game_with_five_players
):
    game, players, players_dict = basic_game_with_five_players
    game._Game__update_players_to_assist(players_dict)

    players[0].streak += "1"
    players[0].round_index += 1

    game._Game__update_players_to_assist(players_dict)

    assert players[0].id not in game.players_to_assist
    assert players[1].id in game.players_to_assist
    assert players[2].id in game.players_to_assist
    assert len(game.players_to_assist) == 2


# TODO: Tets auto_increment_round
