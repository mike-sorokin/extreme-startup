import json

from utils_for_tests import *
from setups_for_tests import *


@with_setup()
def test_index_blank_get(_, cli):
    resp = cli.get("/")
    assert resp.status_code == ALL_GOOD
    assert response_as_dict(resp) == {}


@with_setup()
def test_index_post_blank_game_is_initialized_empty_warmup(_, cli):
    game_json_dict = create_game(cli)
    assert is_valid_game_json(game_json_dict)
    assert game_json_dict["round"] == 0
    assert game_json_dict["players"] == []


@with_setup(create_a_couple_of_games)
def test_index_can_get(extras, cli):
    resp = cli.get("/")
    assert resp.status_code == ALL_GOOD

    # Expected ids
    id_1 = extras[0]["id"]
    id_2 = extras[1]["id"]

    rd = response_as_dict(resp)

    # assert keyset_of(rd).only_contains_the_following_keys(id_1, id_2)
    assert is_valid_game_json(rd[id_1])
    assert is_valid_game_json(rd[id_2])


@with_setup()
def test_index_put_throws_an_error(_, cli):
    resp = cli.put("/")
    assert resp.status_code == ERROR_405


@with_setup(create_a_couple_of_games)
def test_index_delete_drops_all_games(_, cli):
    r = cli.delete("/")
    get_response = cli.get("/")
    assert response_as_dict(get_response) == {}
    assert r.status_code == DELETE_SUCCESS


@with_setup()
def test_game_id_get_does_not_exist(_, cli):
    assert cli.get("/nonexistinggameid").status_code == NOT_FOUND


@with_setup(create_a_game_with_players)
def test_game_id_get_contains_players(extras, cli):
    game_id = extras["game"]["id"]
    response = cli.get(f"/{game_id}")
    assert response.status_code == ALL_GOOD

    rd = response_as_dict(response)

    assert is_valid_game_json(rd)

    # May be redundant since the create_game request validation is within
    # other tests coverage. Keeping it just for sanity.
    assert keyset_of(rd).only_contains_the_following_keys(*set(extras["game"]))
    assert set(rd["players"]) == set(extras["players"])


@with_setup(create_a_game_with_players)
def test_game_id_post_returns_error(extras, cli):
    game_id = extras["game"]["id"]
    resposne = cli.post(f"/{game_id}")
    assert resposne.status_code == ERROR_405


@with_setup(create_a_game_with_players)
def test_game_id_put_advances_round(extras, cli):
    ADVANCED_ROUND_NO = 1
    game_id = extras["game"]["id"]

    update_game_resp = cli.put(f"/{game_id}", data={"round": ADVANCED_ROUND_NO})
    assert update_game_resp.status_code == ALL_GOOD

    get_game_resp = cli.get(f"/{game_id}")

    game_rd = response_as_dict_if_sucecssful(get_game_resp)
    assert game_rd["round"] == ADVANCED_ROUND_NO


@with_setup(create_a_game_with_players)
def test_game_id_delete_removes_the_game(extras, cli):
    game_id = extras["game"]["id"]
    delete_response = cli.delete(f"/{game_id}")
    rd = response_as_dict(delete_response)

    assert keyset_of(rd).only_contains_the_following_keys("deleted")
    assert rd["deleted"] == game_id


@with_setup()
def test_players_get_game_does_not_exist(_, cli):
    response = cli.get("f/nonexistinggameid/players")
    assert response.status_code == NOT_FOUND


@with_setup(create_a_game_with_players, num_players=5)
def test_players_get_fetches_all_players(extras, cli):
    gid = extras["game"]["id"]
    expected_players = extras["players"]
    rd = response_as_dict_if_sucecssful(cli.get(f"/{gid}/players"))
    assert keyset_of(rd).only_contains_the_following_keys("players")
    actual_players = rd["players"]

    # Asserting that the players are the same
    assert set(expected_players) == set(actual_players)

    # Asserting that all players reference the game
    assert all(map(lambda player: player["game_id"] == gid, actual_players.values()))


@with_setup(create_a_game_with_players, num_players=5)
def test_players_post_creates_a_new_player(extras, cli):
    gid = extras["game"]["id"]
    players = extras["players"]
    initial_num_players = len(players)

    response = cli.post(
        f"/{gid}/players",
        data={
            "name": "John_Doe",
            "api": "abc.com",
        },
    )
    rd = response_as_dict_if_sucecssful(response)
    assert is_valid_player_json(rd)
    assert rd["name"] == "John_Doe"
    assert rd["api"] == "abc.com"
    assert rd["game_id"] == gid

    rd = response_as_dict_if_sucecssful(
        cli.get(
            f"/{gid}",
        )
    )
    assert len(rd["players"]) == initial_num_players + 1


@with_setup()
def test_players_put_returns_error_code(_, cli):
    assert cli.put("/nonexistinggameid/players").status_code == ERROR_405


@with_setup(create_a_game_with_players, num_players=5)
def test_players_delete_removes_all_players(extras, cli):
    gid = extras["game"]["id"]
    assert cli.delete(f"/{gid}/players").status_code == DELETE_SUCCESS

    rd = response_as_dict_if_sucecssful(cli.get(f"/{gid}/players"))
    assert not rd["players"]


@with_setup(create_a_game_with_players, num_players=1)
def test_player_id_get_returns_player_json(extras, cli):
    gid = extras["game"]["id"]
    pid = extras["players"][0]["id"]
    rd = response_as_dict_if_sucecssful(cli.get(f"/{gid}/players/{pid}"))
    assert is_valid_player_json(rd)
    assert rd["id"] == pid


@with_setup()
def test_player_id_post_throws_an_error(_, cli):
    assert cli.post("/someid/players/someid").status_code == ERROR_405


@with_setup(create_a_game_with_players)
def test_player_id_put_update_name(extras, cli):
    gid = extras["game"]["id"]
    pid = extras["players"][0]["id"]

    new_name = "John_Doe_Junior"
    rd = response_as_dict_if_sucecssful(
        cli.put(f"/{gid}/players/{pid}"),
        data={
            "name": new_name,
        },
    )
    assert is_valid_player_json(rd)
    assert rd["name"] == new_name


@with_setup(create_a_game_with_players)
def test_player_id_put_update_api(extras, cli):
    gid = extras["game"]["id"]
    pid = extras["players"][0]["id"]

    new_api = "johndoejr.co.uk"
    rd = response_as_dict_if_sucecssful(
        cli.put(f"/{gid}/players/{pid}"),
        data={
            "api": new_api,
        },
    )
    assert is_valid_player_json(rd)
    assert rd["api"] == new_api


@with_setup(create_a_game_with_players)
def test_player_id_put_update_both_name_and_api(extras, cli):
    gid = extras["game"]["id"]
    pid = extras["players"][0]["id"]

    new_name = "John_Doe_Junior"
    new_api = "johndoejr.co.uk"
    rd = response_as_dict_if_sucecssful(
        cli.put(f"/{gid}/players/{pid}"),
        data={
            "name": new_name,
            "api": new_api,
        },
    )
    assert is_valid_player_json(rd)
    assert rd["name"] == new_name
    assert rd["api"] == new_api


@with_setup(create_a_game_with_players)
def test_player_id_delete_removes_the_player(extras, cli):
    gid = extras["game"]["id"]
    pid = extras["players"][0]["id"]
    rd = response_as_dict_if_sucecssful(cli.delete(f"/{gid}/players/{pid}"))

    assert keyset_of(rd).only_contains_the_following_keys("deleted")
    assert rd["deleted"] == pid


@with_setup()
def test_events_post_throws_an_error(_, cli):
    assert cli.post("/someid/players/someid/events").status_code == ERROR_405


@with_setup()
def test_events_put_throws_an_error(_, cli):
    assert cli.put("/someid/players/someid/events").status_code == ERROR_405


@with_setup()
def test_event_id_post_throws_an_error(_, cli):
    assert cli.post("/someid/players/someid/events/someid").status_code == ERROR_405


@with_setup()
def test_event_id_put_throws_an_error(_, cli):
    assert cli.put("/someid/players/someid/events/someid").status_code == ERROR_405
