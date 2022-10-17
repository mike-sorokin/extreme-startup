from enum import Enum
import json

import sys

sys.path.append(".")

from flaskr import app
from utils_for_tests import *


GET = 0
POST = 1
PUT = 2
DELETE = 3


create_a_couple_of_games = ((POST, "/", None, None), (POST, "/", None, None))


def setup_server_with(client, server_setup):
    """Gets a list of tuples representing a request and returns a list of
    corresponding responses"""
    setup_responses = []
    for (method, url, data, query_str) in server_setup:
        get_response_by_request_method = {
            GET: lambda: client.get(url, query_string=query_str),
            POST: lambda: client.post(url, data=data, query_string=query_str),
            PUT: lambda: client.put(url, data=data, query_string=query_str),
            DELETE: lambda: client.delete(url, query_string=query_str),
        }
        rd = response_as_dict(get_response_by_request_method[method]())
        setup_responses.append(rd)
    return setup_responses


def with_setup(server_setup=None):
    """Wrapper for testing functions.
    This sends some pre-emptive "server_setup" requests and does a final
    request, letting the test function verify the response.
    Args:
    - server_setup: a list of tuples corresponding to requests
                    to be sent to server before the test one.
        See setup_server_with"""
    if server_setup is None:
        server_setup = []

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


@with_setup(create_a_couple_of_games)
def test_index_can_get(setups, cli):
    resp = cli.get("/")
    assert resp.status_code == 200

    # Expected ids
    id_1 = setups[0]["id"]
    id_2 = setups[1]["id"]

    rd = response_as_dict(resp)
    assert keyset_of(rd).only_contains_the_following_keys("games")
    assert id_1 in rd["games"]
    assert id_2 in rd["games"]


@with_setup()
def test_index_put_throws_an_error(_, cli):
    resp = cli.put("/")
    assert res.status_code == 501


@with_setup(create_a_couple_of_games)
def test_index_delete_drops_all_games(_, cli):
    cli.delete("/")
    get_response = cli.get("/")
    assert response_as_dict(get_response) == {}
