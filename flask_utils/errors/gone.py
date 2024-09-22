from typing import Optional

from flask_utils.errors.base_class import _BaseFlaskException


class GoneError(_BaseFlaskException):
    """This is the GoneError exception class.

    When raised, it will return a 410 status code with the message and solution provided.

    :param msg: The message to be displayed in the error.
    :type msg: str
    :param solution: The solution to the error.
    :type solution: str

    :Example:

    .. code-block:: python

            from flask_utils.errors import GoneError

            # Inside a Flask route
            @app.route('/example', methods=['POST'])
            def example_route():
                ...
                if some_condition:
                    raise GoneError("This is a gone error.")

    The above code would return the following JSON response from Flask:

    .. code-block:: json

        {
            "success": false,
            "error": {
                "type": "GoneError",
                "name": "Ressource is gone.",
                "message": "This is a gone error.",
                "solution": "Try again later."
            },
            "code": 410
        }

    .. versionadded:: 0.1.0
    """

    def __init__(self, msg: str, solution: Optional[str] = "Try again later.") -> None:
        self.name = "Ressource is gone."
        self.msg = msg
        self.solution = solution
        self.status_code = 410
