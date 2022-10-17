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


def test_players_post_endpoint(arbitrary_player):
    assert arbitrary_player.status_code == 200


def test_can_get_players(client, arbitrary_player):
    """
    On GET request to /players page, should return non-empty dictionary with players
    """
    player_id = arbitrary_player.headers.get("UUID")
    response = client.get("/players")
    player = response.json[player_id]
    assert player["name"] == "John Doe"
    assert player["api"] == "http://172.0.0.1:5050"
