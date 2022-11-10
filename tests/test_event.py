import sys

sys.path.append(".")

from flaskr.event import Event

PLAYER_ID = "dummy_id"
GAME_ID = "game_id"
QUERY = "query"
DIFFICULTY = 0
POINTS_GAINED = 10
RESPONSE_TYPE = "response_type"


def test_event_string_representation_is_correct():
    event = Event(PLAYER_ID, GAME_ID, QUERY, DIFFICULTY, POINTS_GAINED, RESPONSE_TYPE)
    assert (
        event.__str__()
        == f"""
        Player: {PLAYER_ID},
        Game: {GAME_ID},
        Query: {QUERY},
        Difficulty: {DIFFICULTY}
        Points: {POINTS_GAINED}
        Timestamp: {event.timestamp.isoformat()}
        """
    )
