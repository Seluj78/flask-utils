import pytest
from flask import jsonify
from flask import request

from flask_utils import is_it_true


class TestIsItTrueFunction:
    def test_string_true(self):
        assert is_it_true("true") is True

    def test_string_true_uppercase(self):
        assert is_it_true("TRUE") is True

    def test_string_true_yes(self):
        assert is_it_true("yes") is True

    def test_string_true_yes_uppercase(self):
        assert is_it_true("YES") is True

    def test_string_true_one(self):
        assert is_it_true("1") is True

    def test_string_false(self):
        assert is_it_true("false") is False

    def test_string_false_no(self):
        assert is_it_true("no") is False

    def test_string_false_zero(self):
        assert is_it_true("0") is False


class TestIsItTrueInFlask:
    @pytest.fixture(autouse=True)
    def setup(self, flask_client):
        @flask_client.route("/example", methods=["GET"])
        def example():
            is_ordered = request.args.get("is_ordered", type=is_it_true, default=False)
            return jsonify(is_ordered)

    def test_is_ordered_true(self, client):
        response = client.get("example?is_ordered=true")
        assert response.json is True

    def test_is_ordered_true_uppercase(self, client):
        response = client.get("example?is_ordered=TRUE")
        assert response.json is True

    def test_is_ordered_true_yes(self, client):
        response = client.get("example?is_ordered=yes")
        assert response.json is True

    def test_is_ordered_true_yes_uppercase(self, client):
        response = client.get("example?is_ordered=YES")
        assert response.json is True

    def test_is_ordered_true_one(self, client):
        response = client.get("example?is_ordered=1")
        assert response.json is True

    def test_is_ordered_false(self, client):
        response = client.get("example?is_ordered=false")
        assert response.json is False

    def test_is_ordered_false_no(self, client):
        response = client.get("example?is_ordered=no")
        assert response.json is False

    def test_is_ordered_false_zero(self, client):
        response = client.get("example?is_ordered=0")
        assert response.json is False

    def test_is_ordered_default(self, client):
        response = client.get("example")
        assert response.json is False
