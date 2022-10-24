from utils_for_tests import *


def create_game(cli):
    return response_as_dict_if_sucecssful(cli.post("/api", json={}))


def create_player(cli, game_id, player_name="noname", player_url="nourl"):
    return response_as_dict_if_sucecssful(
        cli.post(
            f"/api/{game_id}/players",
            json={"name": player_name, "api": player_url},
        )
    )
