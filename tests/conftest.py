import pytest
from flask import Flask

from flask_utils import register_error_handlers  # Adjust import according to your package structure


@pytest.fixture
def flask_client():
    app = Flask(__name__)
    register_error_handlers(app)
    return app


@pytest.fixture
def client(flask_client):
    with flask_client.test_client() as client:
        yield client
