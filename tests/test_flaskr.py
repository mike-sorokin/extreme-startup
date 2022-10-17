from enum import Enum
from flaskr import app
import json
import pytest

GET = 0
POST = 1
PUT = 2
DELETE = 3

def setup_server_with(client, server_setup):
    for (r, url, data, query_str) in server_setup:
        if r == GET:
            client.get(url, query_string=query_str)

        elif r == POST:
            client.post(url, data=data, query_string=query_str)

        elif r == PUT:
            client.put(url, data=data, query_string=query_str)

        elif r == DELETE:
            client.delete(url, query_string=query_str)

def with_request(
    req_type, 
    url,
    expected_code,
    server_setup=None,
    req_body=None,
    query_str=None,
    ):
    """
    Wrapper for testing functions. This will send a request to the Flask 
    """
    if server_setup is None: server_setup = []

    def inner(test_func):
        def wrapper():
            app.config.update({"TESTING": True})
            client = app.test_client()

            setup_server_with(client, server_setup)

            response = None

            if req_type == GET:
                response = client.get(url, query_string=query_str)

            elif req_type == POST:
                response = client.post(url, data=req_body, query_string=query_str)

            elif req_type == PUT:
                response = client.put(url, data=req_body, query_string=query_str)

            elif req_type == DELETE:
                response = client.delete(url, query_string=query_str)
            
            assert response.status_code == expected_code

            resp_string = response.data.decode("utf-8")
            test_func(json.loads(resp_string))

        return wrapper
    return inner

@with_request(GET, "/", 200)
def test_index_blank_get(response):
    assert response == {}

@with_request(GET, "/", 200, server_setup=[
    (POST, "/", None, None),
    (POST, "/", None, None)
])
def test_index_can_get(response):
    print(response)
    assert len(response.items()) == 2





# @with_request("GET", "/", 200)
# def test_get_index(clientent):
#     """
#     On GET request to index page, should return home page with leaderboard
#     """
#     response = clientent.get("/")
#     assert response.status_code == 200
#     assert "Leaderboard" in response.text


# def test_get_players(clientent):
#     """
#     On GET request to add_player page, should return form with add player name and url
#     """
#     response = clientent.get("/players")
#     assert response.status_code == 200
#     assert "name" in response.text
#     assert "url" in response.text


# def test_post_players(clientent):
#     """
#     On POST request to add_player page, should return player_added page
#     """
#     response = clientent.post("/players", data={"name": "John Doe", "url": "http://172.0.0.1:5050"})
#     player_id = response.headers.get("UUID")
#     assert response.status_code == 200
#     assert "player added" in response.text.lower()
#     response2 = clientent.get(f"/withdraw/{player_id}")
#     assert response2.status_code == 302

