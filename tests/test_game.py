from flaskr.game import Game
import pytest

@pytest.fixture()
def basic_game():
    return Game()

def test_game_initialises_with_no_players(basic_game):
    assert len(basic_game.players) == 0

def test_game_defaults_to_round_zero(basic_game):
    assert basic_game.round == 0

def test_game_can_append_new_players(basic_game):
    basic_game.new_player("dummy_id")
    assert len(basic_game.players) == 1
    assert "dummy_id" in basic_game.players