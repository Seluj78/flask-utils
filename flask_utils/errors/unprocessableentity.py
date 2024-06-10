from flask_utils.errors.base_class import _BaseFlaskException


class UnprocessableEntityError(_BaseFlaskException):
    """This is the UnprocessableEntityError exception class.

    When raised, it will return a 422 status code with the message and solution provided.

    :param msg: The message to be displayed in the error.
    :param solution: The solution to the error.

    :Example:

    .. code-block:: python

            from flask_utils.errors import UnprocessableEntityError

            # Inside a Flask route
            @app.route('/example', methods=['POST'])
            def example_route():
                ...
                if some_condition:
                    raise UnprocessableEntityError("This is an unprocessable entity error.")

    The above code would return the following JSON response from Flask:

    .. code-block:: json

        {
            "success": false,
            "error": {
                "type": "UnprocessableEntityError",
                "name": "Unprocessable Entity",
                "message": "This is an unprocessable entity error.",
                "solution": "Try again."
            },
            "code": 422
        }

    .. versionadded:: 0.1.0
    """

    def __init__(self, msg: str, solution: str = "Try again.") -> None:
        self.name = "Unprocessable Entity"
        self.msg = msg
        self.solution = solution
        self.status_code = 422
