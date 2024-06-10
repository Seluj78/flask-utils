from flask_utils.errors.base_class import _BaseFlaskException


class WebServerIsDownError(_BaseFlaskException):
    """This is the WebServerIsDownError exception class.

    When raised, it will return a 521 status code with the message and solution provided.

    :param msg: The message to be displayed in the error.
    :param solution: The solution to the error.

    :Example:

    .. code-block:: python

            from flask_utils.errors import WebServerIsDownError

            # Inside a Flask route
            @app.route('/example', methods=['POST'])
            def example_route():
                ...
                if some_condition:
                    raise WebServerIsDownError("The web server is down.")

    The above code would return the following JSON response from Flask:

    .. code-block:: json

        {
            "success": false,
            "error": {
                "type": "WebServerIsDownError",
                "name": "Web Server Is Down",
                "message": "The web server is down.",
                "solution": "Try again later."
            },
            "code": 521
        }

    .. versionadded:: 0.1.0
    """

    def __init__(self, msg: str, solution: str = "Try again later.") -> None:
        self.name = "Web Server Is Down"
        self.msg = msg
        self.solution = solution
        self.status_code = 521
