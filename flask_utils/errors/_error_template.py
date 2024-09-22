from flask import Response
from flask import jsonify

from flask_utils.errors.base_class import _BaseFlaskException


def _generate_error_json(error: _BaseFlaskException, status_code: int) -> Response:
    """
    This function is used to generate a json of the error passed

    :param error: The error containing the message and solution
    :type error: _BaseFlaskException

    :param status_code: The status code of the error.
    :type status_code: int

    :return: Returns a json containing all the info
    :rtype: flask.Response

    :Example:

    .. code-block:: python

        from flask_utils.errors import _BaseFlaskException
        from flask_utils.errors._error_template import _generate_error_json

        class MyError(_BaseFlaskException):
            self.name = "MyError"
            self.msg = msg
            self.solution = solution
            self.status_code = 666

        error = MyError("This is an error", "This is the solution")

        json = _generate_error_json(error, 666)

    .. versionadded:: 0.1.0
    """
    success = False
    json = {
        "success": success,
        "error": {
            "type": error.__class__.__name__,
            "name": error.name,
            "message": error.msg,
            "solution": error.solution,
        },
        "code": status_code,
    }
    resp: Response = jsonify(json)
    resp.status_code = status_code
    return resp
