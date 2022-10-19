from utils_for_tests import *


def create_game(cli):
    return response_as_dict_if_sucecssful(cli.post("/"))


def create_player(cli, game_id, player_name="noname", player_url="nourl"):
    return response_as_dict_if_sucecssful(
        cli.post(f"/{game_id}/players", data={"name": player_name, "api": player_url})
    )
