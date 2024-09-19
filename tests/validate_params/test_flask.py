import pytest

from flask_utils import validate_params


class TestBadFormat:
    @pytest.fixture(autouse=True)
    def setup_routes(self, flask_client):
        @flask_client.post("/bad-format")
        @validate_params()
        def bad_format(name: str):
            return "OK", 200

    def test_malformed_body(self, client):
        response = client.post("/bad-format", data="not a json", headers={"Content-Type": "application/json"})
        assert response.status_code == 400

        error_dict = response.get_json()["error"]
        assert error_dict["message"] == "The Json Body is malformed."

    def test_bad_content_type(self, client):
        response = client.post("/bad-format", headers={"Content-Type": "text/plain"}, json={"name": "John"})
        assert response.status_code == 400

        error_dict = response.get_json()["error"]
        assert (
            error_dict["message"]
            == "The Content-Type header is missing or is not set to application/json, or the JSON body is missing."
        )

    def test_missing_body(self, client):
        response = client.post("/bad-format", json={})
        assert response.status_code == 400

        error_dict = response.get_json()["error"]
        assert error_dict["message"] == "Missing json body."

    def test_body_not_dict(self, client):
        response = client.post("/bad-format", json=["not", "a", "dict"])
        assert response.status_code == 400

        error_dict = response.get_json()["error"]
        assert error_dict["message"] == "JSON body must be a dict"

    @pytest.mark.parametrize(
        "key, data",
        [
            (
                "name",
                {
                    "age": 25,
                    "is_active": True,
                    "weight": 70.5,
                    "hobbies": ["reading"],
                    "address": {"city": "New York City"},
                },
            ),
            (
                "age",
                {
                    "name": "John",
                    "is_active": True,
                    "weight": 70.5,
                    "hobbies": ["reading"],
                    "address": {"city": "New York City"},
                },
            ),
            (
                "is_active",
                {
                    "name": "John",
                    "age": 25,
                    "weight": 70.5,
                    "hobbies": ["reading"],
                    "address": {"city": "New York City"},
                },
            ),
            (
                "weight",
                {
                    "name": "John",
                    "age": 25,
                    "is_active": True,
                    "hobbies": ["reading"],
                    "address": {"city": "New York City"},
                },
            ),
            (
                "hobbies",
                {"name": "John", "age": 25, "is_active": True, "weight": 70.5, "address": {"city": "New York City"}},
            ),
            ("address", {"name": "John", "age": 25, "is_active": True, "weight": 70.5, "hobbies": ["reading"]}),
        ],
    )
    def test_missing_key(self, client, key, data):
        response = client.post("/default-types", json=data)
        assert response.status_code == 400

        error_dict = response.get_json()["error"]
        assert error_dict["message"] == f"Missing key: {key}"

    def test_unexpected_key(self, client):
        response = client.post(
            "/default-types",
            json={
                "name": "John",
                "age": 25,
                "is_active": True,
                "weight": 70.5,
                "hobbies": ["reading"],
                "address": {"city": "New York City"},
                "unexpected_key": "value",
            },
        )
        assert response.status_code == 400

        error_dict = response.get_json()["error"]
        assert error_dict["message"] == "Unexpected key: unexpected_key."
