import pytest
from flaskr import app
from flask import Flask


@pytest.fixture()
def test_app():
    app.config.update({"TESTING": True})
    # SETTING UP HERE
    yield app
    # CLEAN UP HERE
    


@pytest.fixture
def client(test_app):
    return test_app.test_client()
