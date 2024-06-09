import pytest

from flask_utils.errors.badrequest import BadRequestError
from flask_utils.errors.conflict import ConflictError
from flask_utils.errors.failed_dependency import FailedDependencyError
from flask_utils.errors.forbidden import ForbiddenError
from flask_utils.errors.gone import GoneError
from flask_utils.errors.notfound import NotFoundError
from flask_utils.errors.origin_is_unreachable import OriginIsUnreachableError
from flask_utils.errors.service_unavailable import ServiceUnavailableError
from flask_utils.errors.unauthorized import UnauthorizedError
from flask_utils.errors.unprocessableentity import UnprocessableEntityError
from flask_utils.errors.web_server_is_down import WebServerIsDownError


@pytest.fixture(autouse=True)
def setup_routes(flask_client):
    @flask_client.route("/bad_request")
    def bad_request():
        raise BadRequestError("Bad request error")

    @flask_client.route("/conflict")
    def conflict():
        raise ConflictError("Conflict error")

    @flask_client.route("/forbidden")
    def forbidden():
        raise ForbiddenError("Forbidden error")

    @flask_client.route("/not_found")
    def not_found():
        raise NotFoundError("Not found error")

    @flask_client.route("/unauthorized")
    def unauthorized():
        raise UnauthorizedError("Unauthorized error")

    @flask_client.route("/origin_is_unreachable")
    def origin_is_unreachable():
        raise OriginIsUnreachableError("Origin is unreachable error")

    @flask_client.route("/web_server_is_down")
    def web_server_is_down():
        raise WebServerIsDownError("Web server is down error")

    @flask_client.route("/failed_dependency")
    def failed_dependency():
        raise FailedDependencyError("Failed dependency error")

    @flask_client.route("/gone")
    def gone():
        raise GoneError("Gone error")

    @flask_client.route("/unprocessable_entity")
    def unprocessable_entity():
        raise UnprocessableEntityError("Unprocessable entity error")

    @flask_client.route("/service_unavailable")
    def service_unavailable():
        raise ServiceUnavailableError("Service unavailable error")


def test_bad_request_error_handler(client):
    response = client.get("/bad_request")
    assert response.status_code == 400

    response_json = response.get_json()
    assert response_json["error"]["message"] == "Bad request error"
    assert response_json["error"]["solution"] == "Try again."
    assert response_json["error"]["name"] == "Bad Request"
    assert response_json["error"]["type"] == "BadRequestError"


def test_conflict_error_handler(client):
    response = client.get("/conflict")
    assert response.status_code == 409

    response_json = response.get_json()
    assert response_json["error"]["message"] == "Conflict error"
    assert response_json["error"]["solution"] == "Try again."
    assert response_json["error"]["name"] == "Conflict"
    assert response_json["error"]["type"] == "ConflictError"


def test_forbidden_error_handler(client):
    response = client.get("/forbidden")
    assert response.status_code == 403

    response_json = response.get_json()
    assert response_json["error"]["message"] == "Forbidden error"
    assert response_json["error"]["solution"] == "Try again."
    assert response_json["error"]["name"] == "Forbidden"
    assert response_json["error"]["type"] == "ForbiddenError"


def test_not_found_error_handler(client):
    response = client.get("/not_found")
    assert response.status_code == 404

    response_json = response.get_json()
    assert response_json["error"]["message"] == "Not found error"
    assert response_json["error"]["solution"] == "Try again."
    assert response_json["error"]["name"] == "Not Found"
    assert response_json["error"]["type"] == "NotFoundError"


def test_unauthorized_error_handler(client):
    response = client.get("/unauthorized")
    assert response.status_code == 401

    response_json = response.get_json()
    assert response_json["error"]["message"] == "Unauthorized error"
    assert response_json["error"]["solution"] == "Try again."
    assert response_json["error"]["name"] == "Unauthorized"
    assert response_json["error"]["type"] == "UnauthorizedError"


def test_origin_is_unreachable_error_handler(client):
    response = client.get("/origin_is_unreachable")
    assert response.status_code == 523

    response_json = response.get_json()
    assert response_json["error"]["message"] == "Origin is unreachable error"
    assert response_json["error"]["solution"] == "Try again later."
    assert response_json["error"]["name"] == "Origin is unreachable"
    assert response_json["error"]["type"] == "OriginIsUnreachableError"


def test_web_server_is_down_error_handler(client):
    response = client.get("/web_server_is_down")
    assert response.status_code == 521

    response_json = response.get_json()
    assert response_json["error"]["message"] == "Web server is down error"
    assert response_json["error"]["solution"] == "Try again later."
    assert response_json["error"]["name"] == "Web Server Is Down"
    assert response_json["error"]["type"] == "WebServerIsDownError"


def test_failed_dependency_error_handler(client):
    response = client.get("/failed_dependency")
    assert response.status_code == 424

    response_json = response.get_json()
    assert response_json["error"]["message"] == "Failed dependency error"
    assert response_json["error"]["solution"] == "Try again later."
    assert response_json["error"]["name"] == "Failed Dependency"
    assert response_json["error"]["type"] == "FailedDependencyError"


def test_gone_error_handler(client):
    response = client.get("/gone")
    assert response.status_code == 410

    response_json = response.get_json()
    assert response_json["error"]["message"] == "Gone error"
    assert response_json["error"]["solution"] == "Try again later."
    assert response_json["error"]["name"] == "Ressource is gone."
    assert response_json["error"]["type"] == "GoneError"


def test_unprocessable_entity_error_handler(client):
    response = client.get("/unprocessable_entity")
    assert response.status_code == 422

    response_json = response.get_json()
    assert response_json["error"]["message"] == "Unprocessable entity error"
    assert response_json["error"]["solution"] == "Try again."
    assert response_json["error"]["name"] == "Unprocessable Entity"
    assert response_json["error"]["type"] == "UnprocessableEntityError"


def test_service_unavailable_error_handler(client):
    response = client.get("/service_unavailable")
    assert response.status_code == 503

    response_json = response.get_json()
    assert response_json["error"]["message"] == "Service unavailable error"
    assert response_json["error"]["solution"] == "Try again later."
    assert response_json["error"]["name"] == "Service Unavailable"
    assert response_json["error"]["type"] == "ServiceUnavailableError"
