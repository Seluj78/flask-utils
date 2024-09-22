from typing import Optional

from flask_utils.errors.base_class import _BaseFlaskException


class BadRequestError(_BaseFlaskException):
    """This is the BadRequestError exception class.

    When raised, it will return a 400 status code with the message and solution provided.

    :param msg: The message to be displayed in the error.
    :type msg: str
    :param solution: The solution to the error.
    :type solution: str

    :Example:

    .. code-block:: python

        from flask_utils.errors import BadRequestError

        # Inside a Flask route
        @app.route('/example', methods=['POST'])
        def example_route():
            ...
            if some_condition:
                raise BadRequestError("This is a bad request error.")

    The above code would return the following JSON response from Flask:

    .. code-block:: json

        {
            "success": false,
            "error": {
                "type": "BadRequestError",
                "name": "Bad Request",
                "message": "This is a bad request error.",
                "solution": "Try again."
            },
            "code": 400
        }

    .. versionadded:: 0.1.0
    """

    def __init__(self, msg: str, solution: Optional[str] = "Try again.") -> None:
        self.name = "Bad Request"
        self.msg = msg
        self.solution = solution
        self.status_code = 400
