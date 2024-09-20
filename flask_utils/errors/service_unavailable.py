from typing import Optional

from flask_utils.errors.base_class import _BaseFlaskException


class ServiceUnavailableError(_BaseFlaskException):
    """This is the ServiceUnavailableError exception class.

    When raised, it will return a 503 status code with the message and solution provided.

    :param msg: The message to be displayed in the error.
    :param solution: The solution to the error.

    :Example:

    .. code-block:: python

            from flask_utils.errors import ServiceUnavailableError

            # Inside a Flask route
            @app.route('/example', methods=['POST'])
            def example_route():
                ...
                if some_condition:
                    raise ServiceUnavailableError("This is a service unavailable error.")

    The above code would return the following JSON response from Flask:

    .. code-block:: json

        {
            "success": false,
            "error": {
                "type": "ServiceUnavailableError",
                "name": "Service Unavailable",
                "message": "This is a service unavailable error.",
                "solution": "Try again later."
            },
            "code": 503
        }

    .. versionadded:: 0.1.0
    """

    def __init__(self, msg: str, solution: Optional[str] = "Try again later.") -> None:
        self.name = "Service Unavailable"
        self.msg = msg
        self.solution = solution
        self.status_code = 503
