from flaskr import app
import json
import pytest

class setup_clientent:
    @staticmethod
    def default(client):
        pass

    @staticmethod
    def one_game(client):
        client.post("/", data={})

def with_request(req_type, url, expected_code, json_req=None, query_str=None, setup_fun=setup_clientent.default):
    def inner(test_func):
        def wrapper():
            app.config.update({"TESTING": True})
            client = app.test_client()

            setup_fun(client)

            response = None
            if req_type == "GET":
                response = client.get(url, query_string=query_str)
            elif req_type == "POST":
                response == client.post(url, data=json_req, query_string=query_str)
            elif req_type == "PUT":
                response == client.put(url, data=json_req, query_string=query_str)
            elif req_type == "DELETE":
                response == client.delete(url, query_string=query_str)
            
            assert response.status_code == expected_code

            print(response.data)
            test_func(json.loads(response.data))

        return wrapper
    return inner

@with_request("GET", "/", 200)
def test_index_blank_get(response):
    assert response == {}





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

