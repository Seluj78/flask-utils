from flask_utils.errors.base_class import _BaseFlaskException


class ForbiddenError(_BaseFlaskException):
    """This is the ForbiddenError exception class.

    When raised, it will return a 403 status code with the message and solution provided.

    :param msg: The message to be displayed in the error.
    :param solution: The solution to the error.

    :Example:

    .. code-block:: python

            from flask_utils.errors import ForbiddenError

            # Inside a Flask route
            @app.route('/example', methods=['POST'])
            def example_route():
                ...
                if some_condition:
                    raise ForbiddenError("This is a forbidden error.")

    The above code would return the following JSON response from Flask:

    .. code-block:: json

        {
            "success": false,
            "error": {
                "type": "ForbiddenError",
                "name": "Forbidden",
                "message": "This is a forbidden error.",
                "solution": "Try again."
            },
            "code": 403
        }

    .. versionadded:: 0.1.0
    """

    def __init__(self, msg: str, solution: str = "Try again.") -> None:
        self.name = "Forbidden"
        self.msg = msg
        self.solution = solution
        self.status_code = 403
