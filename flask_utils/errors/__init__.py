from flask import Flask
from flask import Response

from flask_utils.errors._error_template import generate_error_json
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


def register_error_handlers(application: Flask) -> None:
    @application.errorhandler(BadRequestError)
    def generate_badrequest(error: BadRequestError) -> Response:
        """
        This is the 400 response creator. It will create a 400 response along with
        a custom message and the 400 code

        :param error: The error body
        :return: Returns the response formatted
        """
        return generate_error_json(error, 400)

    @application.errorhandler(ConflictError)
    def generate_conflict(error: ConflictError) -> Response:
        """
        This is the 409 response creator. It will create a 409 response along with
        a custom message and the 409 code

        :param error: The error body
        :return: Returns the response formatted
        """

        return generate_error_json(error, 409)

    @application.errorhandler(ForbiddenError)
    def generate_forbidden(error: ForbiddenError) -> Response:
        """
        This is the 403 response creator. It will create a 403 response along with
        a custom message and the 403 code

        :param error: The error body
        :return: Returns the response formatted
        """

        return generate_error_json(error, 403)

    @application.errorhandler(NotFoundError)
    def generate_notfound(error: NotFoundError) -> Response:
        """
        This is the 404 response creator. It will create a 404 response with
        a custom message and the 404 code.

        :param error: The error body
        :return: Returns the response formatted
        """

        return generate_error_json(error, 404)

    @application.errorhandler(UnauthorizedError)
    def generate_unauthorized(error: UnauthorizedError) -> Response:
        """
        This is the 401 response creator. It will create a 401 response with
        a custom message and the 401 code.

        :param error: The error body
        :return: Returns the response formatted
        """

        return generate_error_json(error, 401)

    @application.errorhandler(OriginIsUnreachableError)
    def generate_origin_is_unreachable(error: OriginIsUnreachableError) -> Response:
        """
        This is the 523 response creator. It will create a 523 response with
        a custom message and the 523 code.

        :param error: The error body
        :return: Returns the response formatted
        """

        return generate_error_json(error, 523)

    @application.errorhandler(WebServerIsDownError)
    def generate_web_server_is_down(error: WebServerIsDownError) -> Response:
        """
        This is the 521 response creator. It will create a 521 response with
        a custom message and the 521 code.

        :param error: The error body
        :return: Returns the response formatted
        """

        return generate_error_json(error, 521)

    @application.errorhandler(FailedDependencyError)
    def generate_failed_dependency(error: FailedDependencyError) -> Response:
        """
        This is the 424 response creator. It will create a 424 response with
        a custom message and the 424 code.

        :param error: The error body
        :return: Returns the response formatted
        """

        return generate_error_json(error, 424)

    @application.errorhandler(GoneError)
    def generate_gone(error: GoneError) -> Response:
        """
        This is the 410 response creator. It will create a 410 response with
        a custom message and the 410 code.

        :param error: The error body
        :return: Returns the response formatted
        """

        return generate_error_json(error, 410)

    @application.errorhandler(UnprocessableEntityError)
    def generate_unprocessable_entity(error: UnprocessableEntityError) -> Response:
        """
        This is the 422 response creator. It will create a 422 response with
        a custom message and the 422 code.

        :param error: The error body
        :return: Returns the response formatted
        """

        return generate_error_json(error, 422)

    @application.errorhandler(ServiceUnavailableError)
    def generate_service_unavailable(error: ServiceUnavailableError) -> Response:
        """
        This is the 503 response creator. It will create a 503 response with
        a custom message and the 503 code.

        :param error: The error body
        :return: Returns the response formatted
        """

        return generate_error_json(error, 503)


__all__ = [
    "BadRequestError",
    "ConflictError",
    "ForbiddenError",
    "NotFoundError",
    "UnauthorizedError",
    "generate_error_json",
    "FailedDependencyError",
    "WebServerIsDownError",
    "OriginIsUnreachableError",
    "GoneError",
    "UnprocessableEntityError",
    "ServiceUnavailableError",
    "register_error_handlers",
]
