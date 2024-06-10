from flask_utils.errors.base_class import _BaseFlaskException


class FailedDependencyError(_BaseFlaskException):
    """This is the FailedDependencyError exception class.

    When raised, it will return a 424 status code with the message and solution provided.

    :param msg: The message to be displayed in the error.
    :param solution: The solution to the error.

    :Example:

    .. code-block:: python

            from flask_utils.errors import FailedDependencyError

            # Inside a Flask route
            @app.route('/example', methods=['POST'])
            def example_route():
                ...
                if some_condition:
                    raise FailedDependencyError("This is a failed dependency error.")

    The above code would return the following JSON response from Flask:

    .. code-block:: json

        {
            "success": false,
            "error": {
                "type": "FailedDependencyError",
                "name": "Failed Dependency",
                "message": "This is a failed dependency error.",
                "solution": "Try again later."
            },
            "code": 424
        }

    .. versionadded:: 0.1.0
    """

    def __init__(self, msg: str, solution: str = "Try again later.") -> None:
        self.name = "Failed Dependency"
        self.msg = msg
        self.solution = solution
        self.status_code = 424
