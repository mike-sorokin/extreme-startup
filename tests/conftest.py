import pytest
import flaskr.__init__
from flaskr import app
from flask import Flask

@pytest.fixture()
def test_app():
    app.config.update({"TESTING": True})
    # SETTING UP HERE
    QUESTION_DELAY = QUESTION_TIMEOUT = 1
    yield app
    # CLEAN UP HERE
    


@pytest.fixture
def client(test_app):
    return test_app.test_client()
