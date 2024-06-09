from flask import jsonify
from flask import Response

from flask_utils.errors.base_class import BaseFlaskException


def generate_error_json(error: BaseFlaskException, status_code: int) -> Response:
    """
    This function is used to generate a json of the error passed

    :param error: The error containing the message and solution
    :param status_code: The status code of the error.
    :return: Returns a json containing all the info
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
