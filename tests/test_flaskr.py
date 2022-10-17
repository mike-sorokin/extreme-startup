from enum import Enum
import json


from utils_for_tests import *
from setups_for_tests import *


@with_setup()
def test_index_blank_get(_, cli):
    resp = cli.get("/")
    assert resp.status_code == ALL_GOOD
    assert response_as_dict(resp) == {}


@with_setup(create_a_couple_of_games)
def test_index_can_get(extras, cli):
    resp = cli.get("/")
    assert resp.status_code == ALL_GOOD

    # Expected ids
    id_1 = extras[0]["id"]
    id_2 = extras[1]["id"]

    rd = response_as_dict(resp)
    assert keyset_of(rd).only_contains_the_following_keys("games")
    assert id_1 in rd["games"]
    assert id_2 in rd["games"]


@with_setup()
def test_index_put_throws_an_error(_, cli):
    resp = cli.put("/")
    assert resp.status_code == ERROR_501


@with_setup(create_a_couple_of_games)
def test_index_delete_drops_all_games(_, cli):
    cli.delete("/")
    get_response = cli.get("/")
    assert response_as_dict(get_response) == {}


@with_setup(create_a_game_with_players)
def test_game_id_contains_players(extras, cli):
    game_id = extras["game"]["id"]
    resposne = cli.get(f"/{game_id}")
    assert response.status_code == ALL_GOOD

    rd = response_as_dict(response)

    assert is_valid_game_json(rd)

    # May be redundant since the create_game request validation is within
    # other tests coverage. Keeping it just for sanity.
    assert keyset_of(rd).only_contains_the_following_keys(*set(extras["game"]))

    assert set(rd["players"]) == set(extras["players"])
