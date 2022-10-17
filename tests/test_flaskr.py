from http import client
from urllib import response
import pytest
import json

def test_get_index(client):
    """
    On GET request to index page, should return home page with leaderboard
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "Leaderboard" in response.text

def test_players_get_endpoint(client):
    """
    On GET request to /players page, should be valid request 
    """
    response = client.get("/players")
    assert response.status_code == 200

@pytest.fixture
def arbitrary_player(client):
    arbitrary_player = client.post("/players", data={"name": "John Doe", "url": "http://172.0.0.1:5050"})
    yield arbitrary_player
    player_id = arbitrary_player.headers.get("UUID")
    client.get(f"/withdraw/{player_id}")

def test_players_post_endpoint(arbitrary_player): 
    assert arbitrary_player.status_code == 200 

def test_can_get_players(client, arbitrary_player):
    """
    On GET request to /players page, should return non-empty dictionary with players
    """
    player_id = arbitrary_player.headers.get("UUID")
    response = client.get("/players")
    player = json.loads(response.text)[player_id]
    assert player['name'] == "John Doe"
    assert player['url'] == "http://172.0.0.1:5050"