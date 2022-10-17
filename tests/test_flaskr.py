from enum import Enum
from urllib import response
from flaskr import app
import json
import pytest

GET = 0
POST = 1
PUT = 2
DELETE = 3

def setup_server_with(client, server_setup):
    setup_responses = []
    for (r, url, data, query_str) in server_setup:
        if r == GET:
            setup_responses.append(
                response_as_dict(client.get(url, query_string=query_str))
                )

        elif r == POST:
            setup_responses.append(
                response_as_dict(client.post(url, data=data, query_string=query_str))
                )

        elif r == PUT:
            setup_responses.append(
                response_as_dict(client.put(url, data=data, query_string=query_str))
                )

        elif r == DELETE:
            setup_responses.append(
                response_as_dict(client.delete(url, query_string=query_str))
                )
    return setup_responses

def response_as_dict(resp):
    return json.loads(resp.data.decode("utf-8"))

def with_setup(
    server_setup=None,
    req_body=None,
    query_str=None,
    ):
    """
    Wrapper for testing functions. This sends some pre-emptive "server_setup" requests
    and does a final request, letting the test function verify the response.
    Args:
    - server_setup: a list of tuples corresponding to requests to be sent to server before the test one.
        See setup_server_with
    - req_body: request body JSON represented as python dict
    - query_str: ?q=... string represented as python dict. 
    """
    if server_setup is None: server_setup = []

    def inner(test_func):
        def wrapper():
            # Connect to our flask app.
            app.config.update({"TESTING": True})
            client = app.test_client()

            # Pre-populate with some requests
            setup_responses = setup_server_with(client, server_setup)

            test_func(setup_responses, client)

        return wrapper
    return inner

@with_setup()
def test_index_blank_get(_, cli):
    resp = cli.get("/")
    assert resp.status_code == 200
    assert response_as_dict(resp) == {}

@with_setup([
    (POST, "/", None, None),
    (POST, "/", None, None)
])
def test_index_can_get(setups, cli):  
    resp = cli.get("/")
    assert resp.status_code == 200

    # Expected ids
    id_1 = setups[0]["id"]
    id_2 = setups[1]["id"]

    rd = response_as_dict(resp)
    assert len(rd.keys()) == 1
    assert "games" in rd
    assert id_1 in rd["games"]
    assert id_2 in rd["games"]


    







