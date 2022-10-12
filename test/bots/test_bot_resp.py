from bot_resp import *


def test_math_response():
    assert math_response("What is 1 + 1?") == "2"
    assert math_response("What is 1 + 0?") == "1"
