import json


def response_as_dict(response):
    return json.loads(response.data.decode("utf-8"))


def response_as_dict_if_sucecssful(response):
    assert response.status_code == 200, f"Got {response.status_code} instead of 200"
    return response_as_dict(response)


class KeysetMatcher:
    """Class for the sake of calling a function via dot notation"""

    def __init__(self, dictionary):
        self.keyset = set(dictionary.keys())

    def only_contains_the_following_keys(self, *keyset):
        return self.keyset == set(keyset)


def keyset_of(response):
    """Smart Constructor for the KeysetMatcher"""

    if type(response) == dict:
        return KeysetMatcher(response)
    return KeysetMatcher(response_as_dict(response))


def is_valid_game_json(response):
    return keyset_of(response).only_contains_the_following_keys(
        "id", "round", "players", "paused"
    )


def is_valid_player_json(response):
    return keyset_of(response).only_contains_the_following_keys(
        "id", "game_id", "name", "score", "api", "events", "streak"
    )


def is_valid_event_json(response):
    return keyset_of(response).only_contains_the_following_keys(
        "id",
        "player_id",
        "query",
        "difficulty",
        "points_gained",
        "response_type",
        "timestamp",
    )
