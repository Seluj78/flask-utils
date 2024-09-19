from typing import Any
from typing import Dict
from typing import List
from typing import Union
from typing import Optional

import pytest

from flask_utils import validate_params


class TestBadFormat:
    @pytest.fixture(autouse=True)
    def setup_routes(self, flask_client):
        @flask_client.post("/bad-format")
        @validate_params({"name": str})
        def bad_format():
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


class TestDefaultTypes:
    @pytest.fixture(autouse=True)
    def setup_routes(self, flask_client):
        @flask_client.post("/default-types")
        @validate_params(
            {
                "name": str,
                "age": int,
                "is_active": bool,
                "weight": float,
                "hobbies": list,
                "address": dict,
            }
        )
        def default_types():
            return "OK", 200

    def test_valid_request(self, client):
        response = client.post(
            "/default-types",
            json={
                "name": "John",
                "age": 25,
                "is_active": True,
                "weight": 70.5,
                "hobbies": ["reading", 1, 6.66, True, False, [1, 2, 3], {"name": "John"}],
                "address": {
                    "city": "New York City",
                    "street": "Main St.",
                    "number": 123,
                    "is_active": True,
                    "hobbies": ["reading", 1, 6.66, True, False, [1, 2, 3], {"name": "John"}],
                },
            },
        )
        assert response.status_code == 200

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

    @pytest.mark.parametrize(
        "key, data",
        [
            (
                "name",
                {
                    "name": 25,
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
                    "age": "25",
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
                    "is_active": "True",
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
                    "weight": "70.5",
                    "hobbies": ["reading"],
                    "address": {"city": "New York City"},
                },
            ),
            (
                "hobbies",
                {
                    "name": "John",
                    "age": 25,
                    "is_active": True,
                    "weight": 70.5,
                    "hobbies": "reading",
                    "address": {"city": "New York City"},
                },
            ),
            (
                "address",
                {
                    "name": "John",
                    "age": 25,
                    "is_active": True,
                    "weight": 70.5,
                    "hobbies": ["reading"],
                    "address": "New York City",
                },
            ),
        ],
    )
    def test_wrong_type(self, client, key, data):
        response = client.post("/default-types", json=data)
        assert response.status_code == 400

        error_dict = response.get_json()["error"]
        assert error_dict["message"] == f"Wrong type for key {key}."


class TestTupleUnion:
    @pytest.fixture(autouse=True)
    def setup_routes(self, flask_client):
        @flask_client.post("/tuple-union")
        @validate_params({"name": (str, int)})
        def union():
            return "OK", 200

    def test_valid_request(self, client):
        response = client.post("/tuple-union", json={"name": "John"})
        assert response.status_code == 200

        response = client.post("/tuple-union", json={"name": 25})
        assert response.status_code == 200

    def test_wrong_type(self, client):
        response = client.post("/tuple-union", json={"name": 25.5})
        assert response.status_code == 400

        error_dict = response.get_json()["error"]
        assert error_dict["message"] == "Wrong type for key name."


class TestUnion:
    @pytest.fixture(autouse=True)
    def setup_routes(self, flask_client):
        @flask_client.post("/union")
        @validate_params({"name": Union[str, int]})
        def union():
            return "OK", 200

    def test_valid_request(self, client):
        response = client.post("/union", json={"name": "John"})
        assert response.status_code == 200

        response = client.post("/union", json={"name": 25})
        assert response.status_code == 200

    def test_wrong_type(self, client):
        response = client.post("/union", json={"name": 25.5})
        assert response.status_code == 400

        error_dict = response.get_json()["error"]
        assert error_dict["message"] == "Wrong type for key name."


class TestOptional:
    @pytest.fixture(autouse=True)
    def setup_routes(self, flask_client):
        @flask_client.post("/optional")
        @validate_params({"name": str, "age": Optional[int]})
        def optional():
            return "OK", 200

    def test_valid_request(self, client):
        response = client.post("/optional", json={"name": "John", "age": 25})
        assert response.status_code == 200

        response = client.post("/optional", json={"name": "John"})
        assert response.status_code == 200

    def test_wrong_type(self, client):
        response = client.post("/optional", json={"name": "John", "age": "25"})
        assert response.status_code == 400

        error_dict = response.get_json()["error"]
        assert error_dict["message"] == "Wrong type for key age."


class TestList:
    @pytest.fixture(autouse=True)
    def setup_routes(self, flask_client):
        @flask_client.post("/list")
        @validate_params({"name": List[str]})
        def list():
            return "OK", 200

    def test_valid_request(self, client):
        response = client.post("/list", json={"name": ["John", "Doe"]})
        assert response.status_code == 200

    def test_wrong_type(self, client):
        response = client.post("/list", json={"name": ["John", 25]})
        assert response.status_code == 400

        error_dict = response.get_json()["error"]
        assert error_dict["message"] == "Wrong type for key name."


class TestDict:
    @pytest.fixture(autouse=True)
    def setup_routes(self, flask_client):
        @flask_client.post("/dict")
        @validate_params({"name": Dict[str, int]})
        def dict_route():
            return "OK", 200

    def test_valid_request(self, client):
        response = client.post("/dict", json={"name": {"John": 25}})
        assert response.status_code == 200

    def test_wrong_type(self, client):
        response = client.post("/dict", json={"name": {"John": "25"}})
        assert response.status_code == 400

        error_dict = response.get_json()["error"]
        assert error_dict["message"] == "Wrong type for key name."


class TestAny:
    @pytest.fixture(autouse=True)
    def setup_routes(self, flask_client):
        @flask_client.post("/any")
        @validate_params({"name": Any})
        def any_route():
            return "OK", 200

    def test_valid_request(self, client):
        response = client.post("/any", json={"name": "John"})
        assert response.status_code == 200

        response = client.post("/any", json={"name": 25})
        assert response.status_code == 200

        response = client.post("/any", json={"name": True})
        assert response.status_code == 200

        response = client.post("/any", json={"name": 25.5})
        assert response.status_code == 200

        response = client.post("/any", json={"name": ["John", 25]})
        assert response.status_code == 200

        response = client.post("/any", json={"name": {"John": 25}})
        assert response.status_code == 200


class TestMixAndMatch:
    @pytest.fixture(autouse=True)
    def setup_routes(self, flask_client):
        @flask_client.post("/mix-and-match")
        @validate_params(
            {
                "name": Union[str, int],
                "age": Optional[int],
                "hobbies": List[str],
                "address": Dict[str, int],
                "is_active": Any,
            }
        )
        def mix_and_match():
            return "OK", 200

    def test_valid_request(self, client):
        response = client.post(
            "/mix-and-match",
            json={"name": "John", "age": 25, "hobbies": ["reading"], "address": {"city": 123}, "is_active": True},
        )
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "key, data, is_missing",
        [
            ("name", {"age": 25, "hobbies": ["reading"], "address": {"city": 123}, "is_active": True}, True),
            ("age", {"name": "John", "hobbies": ["reading"], "address": {"city": 123}, "is_active": True}, False),
            ("hobbies", {"name": "John", "age": 25, "address": {"city": 123}, "is_active": True}, True),
            ("address", {"name": "John", "age": 25, "hobbies": ["reading"], "is_active": True}, True),
            ("is_active", {"name": "John", "age": 25, "hobbies": ["reading"], "address": {"city": 123}}, True),
        ],
    )
    def test_missing_key(self, client, key, data, is_missing):
        response = client.post("/mix-and-match", json=data)

        if not is_missing:
            assert response.status_code == 200
        else:
            assert response.status_code == 400

            error_dict = response.get_json()["error"]
            assert error_dict["message"] == f"Missing key: {key}"

    def test_unexpected_key(self, client):
        response = client.post(
            "/mix-and-match",
            json={
                "name": "John",
                "age": 25,
                "hobbies": ["reading"],
                "address": {"city": 123},
                "is_active": True,
                "unexpected_key": "value",
            },
        )
        assert response.status_code == 400

        error_dict = response.get_json()["error"]
        assert error_dict["message"] == "Unexpected key: unexpected_key."
