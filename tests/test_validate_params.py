import warnings
from typing import Any
from typing import Dict
from typing import List
from typing import Union
from typing import Optional

import pytest
from flask import Flask
from flask import jsonify

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
        response = client.post("/bad-format")
        assert response.status_code == 400

        error_dict = response.get_json()["error"]
        assert (
            error_dict["message"]
            == "The Content-Type header is missing or is not set to application/json, or the JSON body is missing."
        )

    def test_body_not_dict(self, client):
        response = client.post("/bad-format", json=["not", "a", "dict"])
        assert response.status_code == 400

        error_dict = response.get_json()["error"]
        assert error_dict["message"] == "JSON body must be a dict"


class TestDefaultTypes:
    @pytest.fixture(autouse=True)
    def setup_routes(self, flask_client):
        @flask_client.post("/default-types")
        @validate_params()
        def default_types(name: str, age: int, is_active: bool, weight: float, hobbies: list, address: dict):
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
        @validate_params()
        def union(name: (str, int)):
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
        @validate_params()
        def union(name: Union[str, int]):
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
        @validate_params()
        def optional(name: str, age: Optional[int]):
            return "OK", 200

    def test_valid_request(self, client):
        # response = client.post("/optional", json={"name": "John", "age": 25})
        # assert response.status_code == 200

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
        @validate_params()
        def list(name: List[str]):
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
        @validate_params()
        def dict_route(name: Dict[str, int]):
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
        @validate_params()
        def any_route(name: Any):
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
        @validate_params()
        def mix_and_match(
            name: Union[str, int], age: Optional[int], hobbies: List[str], address: Dict[str, int], is_active: Any
        ):
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


class TestValidateParamsWithoutErrorHandlers:
    @pytest.fixture(scope="function")
    def setup_routes(self):
        app = Flask(__name__)
        app.testing = True

        @app.route("/example", methods=["POST", "GET"])
        @validate_params()
        def example(name: str):
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
        @validate_params()
        def example2(name: str, age: int):
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


class TestAnnotationWarnings:
    @pytest.fixture(autouse=True)
    def setup_routes(self, flask_client):
        @flask_client.post("/example/<int:user_id>")
        @validate_params()
        def example(user_id: int, name):
            return "OK", 200

    def test_no_type_annotation(self, client):
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            response = client.post("/example/1", json={"name": "John"})

            assert response.status_code == 200
            assert len(w) == 1
            assert issubclass(w[-1].category, SyntaxWarning)
            assert "Parameter name has no type annotation." in str(w[-1].message)

    def test_duplicate_keys(self, client):
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            response = client.post("/example/1", json={"name": "John", "user_id": 1})

            assert response.status_code == 200
            assert len(w) == 2
            assert issubclass(w[-1].category, SyntaxWarning)
            assert (
                "Parameter user_id is defined in both the route and the JSON body. "
                "The JSON body will override the route parameter." in str(w[-1].message)
            )


class TestMaxDepth:
    @pytest.fixture(autouse=True)
    def setup_routes(self, flask_client):
        @flask_client.post("/example")
        @validate_params()
        def example(user_info: Dict[str, Dict[str, Dict[str, Dict[str, Dict[str, Dict[str, str]]]]]]):
            return "OK", 200

    def test_max_depth(self, client):
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            response = client.post(
                "/example",
                json={
                    "user_info": {
                        "name": {"age": {"is_active": {"weight": {"hobbies": {"address": {"city": "New York City"}}}}}}
                    }
                },
            )

            assert response.status_code == 200
            assert len(w) == 1
            assert issubclass(w[-1].category, SyntaxWarning)
            assert "Maximum depth of 4 reached." in str(w[-1].message)


class TestJSONOverridesRouteParams:
    @pytest.fixture(autouse=True)
    def setup_routes(self, flask_client):
        @flask_client.post("/users/<int:user_id>")
        @validate_params()
        def create_user(user_id: int):
            return f"{user_id}"

    def test_valid_request(self, client):
        response = client.post("/users/123", json={"user_id": 456})
        assert response.status_code == 200
        assert response.text == "456"


class TestEmptyValues:
    @pytest.fixture(autouse=True)
    def setup_routes(self, flask_client):
        @flask_client.route("/empty", methods=["POST"])
        @validate_params()
        def empty_route(name: Optional[str]):
            return jsonify({"name": name})

    def test_empty_value_optional(self, client):
        response = client.post("/empty", json={})
        assert response.status_code == 200
        assert response.get_json() == {"name": None}

        # Testing with 'name' as empty string
        response = client.post("/empty", json={"name": ""})
        assert response.status_code == 200
        assert response.get_json() == {"name": ""}
