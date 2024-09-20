import pytest
from flask import Flask

from flask_utils import validate_params


class TestValidateParamsWithoutErrorHandlers:
    @pytest.fixture(scope="function")
    def setup_routes(self):
        app = Flask(__name__)
        app.testing = True

        @app.route("/example", methods=["POST", "GET"])
        @validate_params({"name": str})
        def example():
            return "OK", 200

        yield app

    @pytest.fixture(autouse=True)
    def client(self, setup_routes):
        yield setup_routes.test_client()

    def test_missing_content_type(self, client):
        response = client.get("/example")
        assert response.status_code == 400
        assert (
            response.json["error"]
            == "The Content-Type header is missing or is not set to application/json, or the JSON body is missing."
        )
        assert "success" not in response.json
        assert "code" not in response.json
        assert not isinstance(response.json["error"], dict)

    def test_malformed_json_body(self, client):
        response = client.post("/example", data="not a json", headers={"Content-Type": "application/json"})
        assert response.status_code == 400
        assert response.json["error"] == "The Json Body is malformed."
        assert "success" not in response.json
        assert "code" not in response.json
        assert not isinstance(response.json["error"], dict)

    def test_json_body_not_dict(self, client):
        response = client.post("/example", json=["not", "a", "dict"])
        assert response.status_code == 400
        assert response.json["error"] == "JSON body must be a dict"
        assert "success" not in response.json
        assert "code" not in response.json
        assert not isinstance(response.json["error"], dict)

    def test_missing_key(self, client, setup_routes):
        @setup_routes.route("/example2", methods=["POST"])
        @validate_params({"name": str, "age": int})
        def example2():
            return "OK", 200

        response = client.post("/example2", json={"name": "John"})
        assert response.status_code == 400
        assert response.json["error"] == "Missing key: age"
        assert "success" not in response.json
        assert "code" not in response.json
        assert not isinstance(response.json["error"], dict)

    def test_unexpected_key(self, client):
        response = client.post("/example", json={"name": "John", "extra": "value"})
        assert response.status_code == 400
        assert response.json["error"] == "Unexpected key: extra."
        assert "success" not in response.json
        assert "code" not in response.json
        assert not isinstance(response.json["error"], dict)

    def test_wrong_type(self, client):
        response = client.post("/example", json={"name": 123})
        assert response.status_code == 400
        assert response.json["error"] == "Wrong type for key name."
        assert "success" not in response.json
        assert "code" not in response.json
        assert not isinstance(response.json["error"], dict)
