from flask import Flask
from flask import Response

from flask_utils.errors.gone import GoneError
from flask_utils.errors.conflict import ConflictError
from flask_utils.errors.notfound import NotFoundError
from flask_utils.errors.forbidden import ForbiddenError
from flask_utils.errors.badrequest import BadRequestError
from flask_utils.errors.unauthorized import UnauthorizedError
from flask_utils.errors._error_template import _generate_error_response
from flask_utils.errors.failed_dependency import FailedDependencyError
from flask_utils.errors.web_server_is_down import WebServerIsDownError
from flask_utils.errors.service_unavailable import ServiceUnavailableError
from flask_utils.errors.unprocessableentity import UnprocessableEntityError
from flask_utils.errors.origin_is_unreachable import OriginIsUnreachableError


def _register_error_handlers(application: Flask) -> None:
    """
    This function will register all the error handlers for the application

    :param application: The Flask application to register the error handlers
    :type application: flask.Flask

    :return: None
    :rtype: None

    .. versionchanged:: 0.5.0
        Made the function private. If you want to register the custom error handlers, you need to
        pass ``register_error_handlers=True`` to the :class:`~flask_utils.extension.FlaskUtils` class
        or to :meth:`~flask_utils.extension.FlaskUtils.init_app`

        register_error_handlers is ``True`` by default.

        .. code-block:: python

            from flask import Flask
            from flask_utils import FlaskUtils

            app = Flask(__name__)
            utils = FlaskUtils(app, register_error_handlers=True)

            # OR

            utils = FlaskUtils()
            utils.init_app(app, register_error_handlers=True)

    .. versionadded:: 0.1.0
    """

    @application.errorhandler(BadRequestError)
    def generate_badrequest(error: BadRequestError) -> Response:
        """
        This is the 400 response creator. It will create a 400 response along with
        a custom message and the 400 code

        :param error: The error body
        :type error: BadRequestError

        :return: Returns the response formatted
        :rtype: flask.Response
        """
        return _generate_error_response(error)

    @application.errorhandler(ConflictError)
    def generate_conflict(error: ConflictError) -> Response:
        """
        This is the 409 response creator. It will create a 409 response along with
        a custom message and the 409 code

        :param error: The error body
        :type error: ConflictError

        :return: Returns the response formatted
        :rtype: flask.Response
        """

        return _generate_error_response(error)

    @application.errorhandler(ForbiddenError)
    def generate_forbidden(error: ForbiddenError) -> Response:
        """
        This is the 403 response creator. It will create a 403 response along with
        a custom message and the 403 code

        :param error: The error body
        :type error: ForbiddenError

        :return: Returns the response formatted
        :rtype: flask.Response
        """

        return _generate_error_response(error)

    @application.errorhandler(NotFoundError)
    def generate_notfound(error: NotFoundError) -> Response:
        """
        This is the 404 response creator. It will create a 404 response with
        a custom message and the 404 code.

        :param error: The error body
        :type error: NotFoundError

        :return: Returns the response formatted
        :rtype: flask.Response
        """

        return _generate_error_response(error)

    @application.errorhandler(UnauthorizedError)
    def generate_unauthorized(error: UnauthorizedError) -> Response:
        """
        This is the 401 response creator. It will create a 401 response with
        a custom message and the 401 code.

        :param error: The error body
        :type error: UnauthorizedError

        :return: Returns the response formatted
        :rtype: flask.Response
        """

        return _generate_error_response(error)

    @application.errorhandler(OriginIsUnreachableError)
    def generate_origin_is_unreachable(error: OriginIsUnreachableError) -> Response:
        """
        This is the 523 response creator. It will create a 523 response with
        a custom message and the 523 code.

        :param error: The error body
        :type error: OriginIsUnreachableError

        :return: Returns the response formatted
        :rtype: flask.Response
        """

        return _generate_error_response(error)

    @application.errorhandler(WebServerIsDownError)
    def generate_web_server_is_down(error: WebServerIsDownError) -> Response:
        """
        This is the 521 response creator. It will create a 521 response with
        a custom message and the 521 code.

        :param error: The error body
        :type error: WebServerIsDownError

        :return: Returns the response formatted
        :rtype: flask.Response
        """

        return _generate_error_response(error)

    @application.errorhandler(FailedDependencyError)
    def generate_failed_dependency(error: FailedDependencyError) -> Response:
        """
        This is the 424 response creator. It will create a 424 response with
        a custom message and the 424 code.

        :param error: The error body
        :type error: FailedDependencyError

        :return: Returns the response formatted
        :rtype: flask.Response
        """

        return _generate_error_response(error)

    @application.errorhandler(GoneError)
    def generate_gone(error: GoneError) -> Response:
        """
        This is the 410 response creator. It will create a 410 response with
        a custom message and the 410 code.

        :param error: The error body
        :type error: GoneError

        :return: Returns the response formatted
        :rtype: flask.Response
        """

        return _generate_error_response(error)

    @application.errorhandler(UnprocessableEntityError)
    def generate_unprocessable_entity(error: UnprocessableEntityError) -> Response:
        """
        This is the 422 response creator. It will create a 422 response with
        a custom message and the 422 code.

        :param error: The error body
        :type error: UnprocessableEntityError

        :return: Returns the response formatted
        :rtype: flask.Response
        """

        return _generate_error_response(error)

    @application.errorhandler(ServiceUnavailableError)
    def generate_service_unavailable(error: ServiceUnavailableError) -> Response:
        """
        This is the 503 response creator. It will create a 503 response with
        a custom message and the 503 code.

        :param error: The error body
        :type error: ServiceUnavailableError

        :return: Returns the response formatted
        :rtype: flask.Response
        """

        return _generate_error_response(error)


__all__ = [
    "BadRequestError",
    "ConflictError",
    "ForbiddenError",
    "NotFoundError",
    "UnauthorizedError",
    "_generate_error_response",
    "FailedDependencyError",
    "WebServerIsDownError",
    "OriginIsUnreachableError",
    "GoneError",
    "UnprocessableEntityError",
    "ServiceUnavailableError",
    "_register_error_handlers",
]
