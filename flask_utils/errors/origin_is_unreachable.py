from typing import Optional

from flask_utils.errors.base_class import _BaseFlaskException


class OriginIsUnreachableError(_BaseFlaskException):
    """This is the OriginIsUnreachableError exception class.

    When raised, it will return a 523 status code with the message and solution provided.

    :param msg: The message to be displayed in the error.
    :type msg: str
    :param solution: The solution to the error.
    :type solution: str

    :Example:

    .. code-block:: python

            from flask_utils.errors import OriginIsUnreachableError

            # Inside a Flask route
            @app.route('/example', methods=['POST'])
            def example_route():
                ...
                if some_condition:
                    raise OriginIsUnreachableError("The origin is unreachable.")

    The above code would return the following JSON response from Flask:

    .. code-block:: json

        {
            "success": false,
            "error": {
                "type": "OriginIsUnreachableError",
                "name": "Origin is unreachable",
                "message": "The origin is unreachable.",
                "solution": "Try again later."
            },
            "code": 523
        }

    .. versionadded:: 0.1.0
    """

    def __init__(self, msg: str, solution: Optional[str] = "Try again later.") -> None:
        self.name = "Origin is unreachable"
        self.msg = msg
        self.solution = solution
        self.status_code = 523
