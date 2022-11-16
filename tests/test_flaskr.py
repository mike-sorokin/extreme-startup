import json

from utils_for_tests import *
from setups_for_tests import *
from unittest.mock import patch

@with_setup()
def test_index_blank_get(_, cli):
    resp = cli.get("/api/")
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
    resp = cli.get("/api")

    assert resp.status_code == ALL_GOOD

    # Expected ids
    id_1 = extras[0]["id"]
    id_2 = extras[1]["id"]

    rd = response_as_dict(resp)

    # assert keyset_of(rd)json={"api": new_api}.only_contains_the_following_keys(id_1, id_2)
    assert is_valid_game_json(rd[id_1])
    assert is_valid_game_json(rd[id_2])


@with_setup()
def test_index_put_throws_an_error(_, cli):
    resp = cli.put("/api/")
    assert resp.status_code == ERROR_405


@with_setup(create_a_couple_of_games)
def test_index_delete_drops_all_games(extras, cli):
    r = cli.delete("/api")
    get_response = cli.get("/api")
    assert response_as_dict(get_response) == {}
    assert r.status_code == DELETE_SUCCESS


@with_setup()
def test_game_id_get_does_not_exist(_, cli):
    assert cli.get("/api/nonexistinggameid/").status_code == NOT_ACCEPTED


@with_setup(create_a_game_with_players)
def test_game_id_get_contains_players(extras, cli):
    game_id = extras["game"]["id"]
    response = cli.get(f"/api/{game_id}/")
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
    resposne = cli.post(f"/api/{game_id}/")
    assert resposne.status_code == ERROR_405


@with_setup(create_a_game_with_players)
def test_game_id_put_advances_round(extras, cli):
    ADVANCED_ROUND_NO = 1
    game_id = extras["game"]["id"]

    update_game_resp = cli.put(f"/api/{game_id}/", json={"round": ADVANCED_ROUND_NO})
    assert update_game_resp.status_code == ALL_GOOD

    get_game_resp = cli.get(f"/api/{game_id}/")

    game_rd = response_as_dict_if_sucecssful(get_game_resp)
    assert game_rd["round"] == ADVANCED_ROUND_NO


@with_setup(create_a_game_with_players)
def test_game_id_delete_removes_the_game(extras, cli):
    game_id = extras["game"]["id"]
    delete_response = cli.delete(f"/api/{game_id}/")
    rd = response_as_dict(delete_response)

    assert keyset_of(rd).only_contains_the_following_keys("deleted")
    assert rd["deleted"] == game_id


@with_setup()
def test_players_get_game_does_not_exist(_, cli):
    response = cli.get("/api/nonexistinggameid/players/")
    assert response.status_code == NOT_ACCEPTED


@with_setup(create_a_game_with_players, num_players=5)
def test_players_get_fetches_all_players(extras, cli):
    gid = extras["game"]["id"]
    expected_players = extras["players"]
    rd = response_as_dict_if_sucecssful(cli.get(f"/api/{gid}/players/"))
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
        f"/api/{gid}/players", json={"name": "John_Doe", "api": "abc.com"}
    )
    rd = response_as_dict_if_sucecssful(response)
    assert is_valid_player_json(rd)
    assert rd["name"] == "John_Doe"
    assert rd["api"] == "abc.com"
    assert rd["game_id"] == gid

    rd = response_as_dict_if_sucecssful(cli.get(f"/api/{gid}/"))
    assert len(rd["players"]) == initial_num_players + 1


@with_setup()
def test_players_put_returns_error_code(_, cli):
    assert cli.put("/api/nonexistinggameid/players/").status_code == ERROR_405


@with_setup(create_a_game_with_players, num_players=5)
def test_players_delete_removes_all_players(extras, cli):
    gid = extras["game"]["id"]
    assert cli.delete(f"/api/{gid}/players/").status_code == DELETE_SUCCESS

    rd = response_as_dict_if_sucecssful(cli.get(f"/api/{gid}/players/"))
    assert not rd["players"]


@with_setup(create_a_game_with_players, num_players=1)
def test_player_id_get_returns_player_json(extras, cli):
    gid = extras["game"]["id"]
    pid = list(extras["players"].keys())[0]
    rd = response_as_dict_if_sucecssful(cli.get(f"/api/{gid}/players/{pid}/"))
    assert is_valid_player_json(rd)
    assert rd["id"] == pid


@with_setup()
def test_player_id_post_throws_an_error(_, cli):
    assert cli.post("/api/someid/players/someid/").status_code == ERROR_405


@with_setup(create_a_game_with_players)
def test_player_id_put_update_name(extras, cli):
    gid = extras["game"]["id"]
    pid = list(extras["players"].keys())[0]

    new_name = "John_Doe_Junior"
    rd = response_as_dict_if_sucecssful(
        cli.put(f"/api/{gid}/players/{pid}/", json={"name": new_name})
    )
    assert is_valid_player_json(rd)
    assert rd["name"] == new_name


@with_setup(create_a_game_with_players)
def test_player_id_put_update_api(extras, cli):
    gid = extras["game"]["id"]
    pid = list(extras["players"].keys())[0]

    new_api = "johndoejr.co.uk"
    rd = response_as_dict_if_sucecssful(
        cli.put(f"/api/{gid}/players/{pid}/", json={"api": new_api})
    )
    assert is_valid_player_json(rd)
    assert rd["api"] == new_api


@with_setup(create_a_game_with_players)
def test_player_id_put_update_both_name_and_api(extras, cli):
    gid = extras["game"]["id"]
    pid = list(extras["players"].keys())[0]

    new_name = "John_Doe_Junior"
    new_api = "johndoejr.co.uk"
    rd = response_as_dict_if_sucecssful(
        cli.put(f"/api/{gid}/players/{pid}/", json={"name": new_name, "api": new_api})
    )
    assert is_valid_player_json(rd)
    assert rd["name"] == new_name
    assert rd["api"] == new_api


@with_setup(create_a_game_with_players)
def test_player_id_delete_removes_the_player(extras, cli):
    gid = extras["game"]["id"]
    pid = list(extras["players"].keys())[0]
    rd = response_as_dict(cli.delete(f"/api/{gid}/players/{pid}"))
    assert keyset_of(rd).only_contains_the_following_keys("deleted")
    assert rd["deleted"] == pid


@with_setup()
def test_events_post_throws_an_error(_, cli):
    assert cli.post("/api/someid/players/someid/events/").status_code == ERROR_405


@with_setup()
def test_events_put_throws_an_error(_, cli):
    assert cli.put("/api/someid/players/someid/events/").status_code == ERROR_405


@with_setup()
def test_event_id_post_throws_an_error(_, cli):
    assert (
        cli.post("/api/someid/players/someid/events/someid/").status_code == ERROR_405
    )


@with_setup()
def test_event_id_put_throws_an_error(_, cli):
    assert cli.put("/api/someid/players/someid/events/someid").status_code == ERROR_405


@with_setup()
def test_auth_put_throws_an_error(_, cli):
    assert cli.put("/api/someid/auth").status_code == ERROR_405


@with_setup()
def test_auth_delete_throws_an_error(_, cli):
    assert cli.delete("/api/someid/auth").status_code == ERROR_405


@with_setup(create_a_single_game)
def test_auth_get_is_authorized_for_admin(extras, cli):
    assert response_as_dict(cli.get(f"/api/{extras[0]['id']}/auth"))["authorized"]


@with_setup(create_a_single_game)
def test_auth_get_is_not_authorized_for_non_admin(extras, cli):
    cli.cookie_jar.clear()
    assert not response_as_dict(cli.get(f"/api/{extras[0]['id']}/auth"))["authorized"]


@with_setup(create_a_single_game)
def test_auth_post_requires_password(extras, cli):
    faulty_auth_request = cli.post(f"/api/{extras[0]['id']}/auth", json={})
    assert faulty_auth_request.status_code == NOT_ACCEPTED


@with_setup(create_a_single_game)
def test_auth_post_with_valid_game_password_returns_valid(extras, cli):
    auth_request = cli.post(
        f"/api/{extras[0]['id']}/auth", json={"password": "dummy_password"}
    )
    assert response_as_dict(auth_request)["valid"]


@with_setup(create_a_single_game)
def test_auth_post_with_invalid_game_password_returns_invalid(extras, cli):
    auth_request = cli.post(
        f"/api/{extras[0]['id']}/auth", json={"password": "incorrect_dummy_password"}
    )
    assert not response_as_dict(auth_request)["valid"]


@with_setup()
def test_game_creation_requires_password(_, cli):
    empty_request = cli.post(f"/api", json={})
    assert empty_request.status_code == NOT_ACCEPTED

    with patch("flaskr.session", dict()) as session:
        request_with_password = cli.post(f"/api", json={"password": "password"})
        assert request_with_password.status_code == ALL_GOOD

        r_dict = response_as_dict(request_with_password)
        assert r_dict["id"] in session.get("admin")


@with_setup(create_a_single_game)
def test_auth_get_returns_true_if_authorized(extras, cli):
    auth_check = response_as_dict_if_sucecssful(cli.get(f"/api/{extras[0]['id']}/auth"))
    assert auth_check["authorized"]


@with_setup(create_a_single_game)
def test_auth_get_returns_false_if_unauthorized(extras, cli):
    cli.cookie_jar.clear()
    auth_check = response_as_dict_if_sucecssful(cli.get(f"/api/{extras[0]['id']}/auth"))
    assert not auth_check["authorized"]


@with_setup(create_a_single_game)
def test_auth_post_fail_when_password_incorrect(extras, cli):
    game_id = extras[0]["id"]
    auth_request = response_as_dict(
        cli.post(f"/api/{game_id}/auth", json={"password": "wrong_password"})
    )
    assert not auth_request["valid"]


@with_setup(create_a_single_game)
def test_auth_post_success_when_credential_correct(extras, cli):
    game_id = extras[0]["id"]

    with patch("flaskr.session", dict()) as session:
        auth_request = response_as_dict_if_sucecssful(
            cli.post(f"/api/{game_id}/auth", json={"password": "dummy_password"})
        )
        assert auth_request["valid"]
        assert game_id in session.get("admin")


@with_setup(create_a_single_game)
def test_admin_of_game_can_delete_game(extras, cli):
    game_id = extras[0]["id"]
    cli.cookie_jar.clear()
    non_admin_request = cli.delete(f"/api/{game_id}")
    assert non_admin_request.status_code == UNAUTHORIZED


@with_setup(create_a_single_game)
def test_non_admin_of_game_can_not_delete_game(extras, cli):
    game_id = extras[0]["id"]
    cli.cookie_jar.clear()

    with patch("flaskr.session", dict()) as session:
        cli.post(f"/api/{game_id}/auth", json={"password": "dummy_password"})
        rd = response_as_dict_if_sucecssful(cli.delete(f"/api/{game_id}"))
        assert keyset_of(rd).only_contains_the_following_keys("deleted")
        assert rd["deleted"] == game_id


@with_setup(create_a_couple_of_games)
def test_admin_of_all_games_can_delete_all_games(extras, cli):
    delete_request = cli.delete("/api")
    assert delete_request.status_code == DELETE_SUCCESS

    rem_games = response_as_dict_if_sucecssful(cli.get("/api"))
    assert not rem_games


@with_setup(create_a_couple_of_games)
def test_non_admin_of_all_games_cannot_delete_all_games(extras, cli):
    id_1 = extras[0]["id"]
    id_2 = extras[1]["id"]

    cli.cookie_jar.clear()

    # authorize as admin for <id_1> game ONLY
    cli.post(f"/api/{id_1}/auth", json={"password": "dummy_password"})

    delete_request = cli.delete("/api")
    assert delete_request.status_code == UNAUTHORIZED

    rem_games = response_as_dict_if_sucecssful(cli.get("/api"))
    assert len(rem_games) == 2


@with_setup(create_a_single_game)
def test_non_admin_of_game_cannot_update_game(extras, cli):
    game_id = extras[0]["id"]
    cli.cookie_jar.clear()
    non_admin_request = cli.put(f"/api/{game_id}", json={"round": 1})
    assert non_admin_request.status_code == UNAUTHORIZED

    non_admin_request = cli.put(f"/api/{game_id}", json={"pause": True})
    assert non_admin_request.status_code == UNAUTHORIZED


@with_setup(create_a_single_game)
def test_admin_of_game_can_update_game(extras, cli):
    game_id = extras[0]["id"]
    cli.cookie_jar.clear()

    with patch("flaskr.session", dict()) as session:
        cli.post(f"/api/{game_id}/auth", json={"password": "dummy_password"})
        admin_request = cli.put(f"/api/{game_id}", json={"round": 1})
        assert admin_request.status_code == ALL_GOOD


@with_setup(create_a_game_with_players)
def test_admin_of_game_can_update_player_fields(extras, cli):
    player1_id = list(extras["players"].keys())[0]
    player1_dict = extras["players"][player1_id]
    cli.cookie_jar.clear()  # clear all cookies
    cli.post(f"/api/{extras['game']['id']}/auth", json={"password": "dummy_password"})

    assert player1_dict["name"] == "noname"  # noname == default_name upon creation

    cli.put(
        f"/api/{extras['game']['id']}/players/{player1_id}",
        json={"name": "updated_name"},
    )
    r2 = response_as_dict(cli.get(f"/api/{extras['game']['id']}/players/{player1_id}"))

    assert r2["name"] == "updated_name"
    assert player1_dict["api"] == "nourl"  # nourl == default api upon creation

    cli.put(
        f"/api/{extras['game']['id']}/players/{player1_id}", json={"api": "updated_api"}
    )
    r2 = response_as_dict(cli.get(f"/api/{extras['game']['id']}/players/{player1_id}"))

    assert r2["api"] == "updated_api"


@with_setup(create_a_single_game)
def test_player_but_not_admin_of_game_can_update_own_player_fields(extras, cli):
    cli.cookie_jar.clear()  # clear all cookies
    player = response_as_dict(
        cli.post(
            f"/api/{extras[0]['id']}/players", json={"name": "noname", "api": "nourl"}
        )
    )

    assert not response_as_dict(cli.get(f"/api/{extras[0]['id']}/auth"))["authorized"]
    assert player["name"] == "noname"  # noname == default_name upon creation
    assert player["api"] == "nourl"

    cli.put(
        f"/api/{extras[0]['id']}/players/{player['id']}",
        json={"name": "updated_name", "api": "updated_api"},
    )
    updated_player = response_as_dict(
        cli.get(f"/api/{extras[0]['id']}/players/{player['id']}")
    )

    assert updated_player["name"] == "updated_name"
    assert updated_player["api"] == "updated_api"


@with_setup(create_a_single_game)
def test_admin_can_delete_player(extras, cli):
    player = response_as_dict(
        cli.post(
            f"/api/{extras[0]['id']}/players", json={"name": "noname", "api": "nourl"}
        )
    )
    cli.cookie_jar.clear()
    cli.post(f"/api/{extras[0]['id']}/auth", json={"password": "dummy_password"})
    delete_request = cli.delete(f"/api/{extras[0]['id']}/players/{player['id']}")

    assert delete_request.status_code == ALL_GOOD

    get_player_request = cli.get(f"/api/{extras[0]['id']}/players/{player['id']}")
    assert get_player_request.status_code == NOT_ACCEPTED


@with_setup(create_a_single_game)
def test_player_can_delete_itself(extras, cli):
    cli.cookie_jar.clear()
    player = response_as_dict(
        cli.post(
            f"/api/{extras[0]['id']}/players", json={"name": "noname", "api": "nourl"}
        )
    )
    delete_request = cli.delete(f"/api/{extras[0]['id']}/players/{player['id']}")

    assert delete_request.status_code == ALL_GOOD

    get_player_request = cli.get(f"/api/{extras[0]['id']}/players/{player['id']}")
    assert get_player_request.status_code == NOT_ACCEPTED


@with_setup(create_a_single_game)
def test_admin_can_delete_all_players(extras, cli):
    for _ in range(10):
        response_as_dict(
            cli.post(
                f"/api/{extras[0]['id']}/players",
                json={"name": "noname", "api": "nourl"},
            )
        )

    cli.cookie_jar.clear()
    cli.post(f"/api/{extras[0]['id']}/auth", json={"password": "dummy_password"})
    delete_request = cli.delete(f"/api/{extras[0]['id']}/players")

    assert delete_request.status_code == DELETE_SUCCESS

    get_player_request = response_as_dict(cli.get(f"/api/{extras[0]['id']}/players"))
    assert not get_player_request["players"]


@with_setup(create_a_single_game)
def test_non_admin_can_not_delete_all_players(extras, cli):
    for _ in range(10):
        response_as_dict(
            cli.post(
                f"/api/{extras[0]['id']}/players",
                json={"name": "noname", "api": "nourl"},
            )
        )

    cli.cookie_jar.clear()
    delete_request = cli.delete(f"/api/{extras[0]['id']}/players")

    assert delete_request.status_code == UNAUTHORIZED

    get_player_request = response_as_dict(cli.get(f"/api/{extras[0]['id']}/players"))
    assert len(get_player_request["players"]) == 10


@with_setup(create_a_single_game)
def test_player_can_delete_itself(extras, cli):
    cli.cookie_jar.clear()
    player = response_as_dict(
        cli.post(
            f"/api/{extras[0]['id']}/players", json={"name": "noname", "api": "nourl"}
        )
    )
    delete_request = cli.delete(f"/api/{extras[0]['id']}/players/{player['id']}")

    assert delete_request.status_code == ALL_GOOD

    get_player_request = cli.get(f"/api/{extras[0]['id']}/players/{player['id']}")
    assert get_player_request.status_code == NOT_ACCEPTED


@with_setup(create_a_single_game)
def test_index_put_throws_an_error(extras, cli):
    resp = cli.get(f"/api/{extras[0]['id']}/assist")

    assert resp.status_code == ALL_GOOD
    assert type(resp.json) is list