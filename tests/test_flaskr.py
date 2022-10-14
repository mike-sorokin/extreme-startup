from http import client
from urllib import response
import pytest


def test_get_index(client):
    """
    On GET request to index page, should return home page with leaderboard
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "Leaderboard" in response.text


def test_get_players(client):
    """
    On GET request to add_player page, should return form with add player name and url
    """
    response = client.get("/players")
    assert response.status_code == 200
    assert "name" in response.text
    assert "url" in response.text


def test_post_players(client):
    """
    On POST request to add_player page, should return player_added page
    """
    response = client.post(
        "/players", data={"name": "John Doe", "url": "http://172.0.0.1:5050"}
    )
    player_id = response.headers.get("UUID")
    assert response.status_code == 200
    assert "player added" in response.text.lower()
    response2 = client.post(f"/withdraw/{player_id}")
    assert response2.status_code == 200
