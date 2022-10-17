import pytest
# from flaskr.__init__ import QUESTION_DELAY, QUESTION_TIMEOUT, game_id, dummy
import flaskr
from flaskr import app
from flask import Flask


@pytest.fixture()
def test_app():
    app.config.update({"TESTING": True})
    # SETTING UP HERE
    flaskr.QUESTION_DELAY = flaskr.QUESTION_TIMEOUT = 0.5
    flaskr.game_id = "dummy_game"
    yield app
    # CLEAN UP HERE


@pytest.fixture
def client(test_app):
    return test_app.test_client()


@pytest.fixture
def arbitrary_player(client):
    arbitrary_player = client.post(
        "/players", data={"name": "John Doe", "url": "http://172.0.0.1:5050"})
    yield arbitrary_player
    player_id = arbitrary_player.headers.get("UUID")
    client.get(f"/withdraw/{player_id}")

