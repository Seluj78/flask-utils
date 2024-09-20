from flask import Flask

from flask_utils import validate_params


def test_validate_params_without_error_handlers():
    app = Flask(__name__)
    app.testing = True

    @app.route("/example")
    @validate_params({"name": str})
    def example():
        return "OK", 200

    response = app.test_client().get("/example")
    assert response.status_code == 400
    assert (
        response.json["error"]
        == "The Content-Type header is missing or is not set to application/json, or the JSON body is missing."
    )
    assert "success" not in response.json
    assert "code" not in response.json
    assert not isinstance(response.json["error"], dict)


# TODO: Test all possible errors that can be raised by validate_params
