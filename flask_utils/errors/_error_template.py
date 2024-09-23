from typing import Any
from typing import Dict

from flask import Response
from flask import jsonify

from flask_utils.errors.base_class import _BaseFlaskException


def _generate_error_dict(error: _BaseFlaskException) -> Dict[str, Any]:
    """
    This function is used to generate a dict of the error passed

    :param error: The error containing the message and solution
    :type error: _BaseFlaskException

    :return: Returns a dict containing a json representation of the error
    :rtype: dict

    :Example:

    .. code-block:: python

        from flask_utils import ConflictError  # or any other error
        from flask_utils.errors._error_template import _generate_error_json

        json = _generate_error_json(error)
        # Sample output:
        # {
        #     "success": False,
        #     "error": {
        #         "type": "ConflictError",
        #         "name": "ConflictError",
        #         "message": "This is the message",
        #         "solution": "This is the solution"
        #     },
        #     "code": 409
        # }

    .. versionadded:: 0.8.0
    """

    return {
        "success": False,
        "error": {
            "type": error.__class__.__name__,
            "name": error.name,
            "message": error.msg,
            "solution": error.solution,
        },
        "code": error.status_code,
    }


def _generate_error_response(error: _BaseFlaskException) -> Response:
    """
    This function is used to generate a json of the error passed

    :param error: The error containing the message and solution
    :type error: _BaseFlaskException

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

    .. versionchanged:: 0.8.0
        This function was renamed from ``generate_error_json`` to ``_generate_error_response``.
        It now returns a ``flask.Response`` object, calling
        :func:`~flask_utils.errors._error_template._generate_error_json` to generate the json.

    .. versionadded:: 0.1.0
    """
    json = _generate_error_dict(error)
    resp: Response = jsonify(json)
    resp.status_code = error.status_code
    return resp
