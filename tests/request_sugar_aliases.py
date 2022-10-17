from utils_for_tests import *


def response_as_dict_if_sucecssful(response):
    assert response.status_code == 200, f"Got {response.status_code} instead of 200"
    return response_as_dict(response)


def create_game(cli):
    return response_as_dict_if_sucecssful(cli.post("/"))


def create_player(cli, game_id, player_name="noname", player_url="nourl"):
    return response_as_dict_if_sucecssful(
        cli.post(
            f"/{game_id}/players",
            data={
                "name": player_name,
                "api": player_url,
            },
        )
    )
