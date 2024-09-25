from typing import Optional

from flask_utils.errors.base_class import _BaseFlaskException


class MethodNotAllowedError(_BaseFlaskException):
    """This is the MethodNotAllowedError exception class.

    When raised, it will return 405 status code with the message and solution provided.

    :param msg: The message to be displayed in the error.
    :type msg: str
    :param solution: The solution to the error.
    :type solution: Optional[str]

    :Example:

    .. code-block:: python

            from flask_utils.errors import MethodNotAllowedError

            # Inside a Flask route
            @app.route('/example', methods=['POST'])
            def example_route():
                ...
                if some_condition:
                    raise MethodNotAllowedError("This is a not allowed error.")

    The above code would return the following JSON response from Flask:

    .. code-block:: json

        {
            "success": false,
            "error": {
                "type": "Method Not Allowed",
                "name": "Method Not Allowed",
                "message": "This is a Method Not Allowed error.",
                "solution": "Try again."
            },
            "code": 404
        }

    .. versionadded:: 0.1.0
    """

    def __init__(self, msg: str, solution: Optional[str] = "Try again.") -> None:
        self.name = "Method Not Allowed"
        self.msg = msg
        self.solution = solution
        self.status_code = 405
