from flaskr.player import Player
from unittest.mock import MagicMock, Mock
import pytest

GAME_ID = 1 
PLAYER_NAME = "dummy_player"
API = "test_url.com"

@pytest.fixture()
def dummy_player():
    return Player(GAME_ID, PLAYER_NAME, API)

def test_player_initialises_correctly(dummy_player):
    assert dummy_player.name == PLAYER_NAME
    assert dummy_player.api == API
    assert dummy_player.game_id == GAME_ID
    assert dummy_player.score == 0
    assert dummy_player.active == True 

def test_player_can_log_event():
    player, event = Player(GAME_ID, PLAYER_NAME, API), Mock()
    assert len(player.events) == 0
    player.log_event(event)
    assert len(player.events) == 1


