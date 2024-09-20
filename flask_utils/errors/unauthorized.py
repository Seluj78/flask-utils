from typing import Optional

from flask_utils.errors.base_class import _BaseFlaskException


class UnauthorizedError(_BaseFlaskException):
    """This is the UnauthorizedError exception class.

    When raised, it will return a 401 status code with the message and solution provided.

    :param msg: The message to be displayed in the error.
    :param solution: The solution to the error.

    :Example:

    .. code-block:: python

            from flask_utils.errors import UnauthorizedError

            # Inside a Flask route
            @app.route('/example', methods=['POST'])
            def example_route():
                ...
                if some_condition:
                    raise UnauthorizedError("This is an unauthorized error.")

    The above code would return the following JSON response from Flask:

    .. code-block:: json

        {
            "success": false,
            "error": {
                "type": "UnauthorizedError",
                "name": "Unauthorized",
                "message": "This is an unauthorized error.",
                "solution": "Try again."
            },
            "code": 401
        }

    .. versionadded:: 0.1.0
    """

    def __init__(self, msg: str, solution: Optional[str] = "Try again.") -> None:
        self.name = "Unauthorized"
        self.msg = msg
        self.solution = solution
        self.status_code = 401
