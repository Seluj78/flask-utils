import pytest
from flask import Flask

from flask_utils import FlaskUtils  # Adjust import according to your package structure


@pytest.fixture
def flask_client():
    app = Flask(__name__)
    FlaskUtils(app)
    return app


@pytest.fixture
def client(flask_client):
    with flask_client.test_client() as client:
        yield client
