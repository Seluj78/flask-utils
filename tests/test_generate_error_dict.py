import pytest

from flask_utils import MethodNotAllowedError
from flask_utils.errors import GoneError
from flask_utils.errors import ConflictError
from flask_utils.errors import NotFoundError
from flask_utils.errors import ForbiddenError
from flask_utils.errors import BadRequestError
from flask_utils.errors import UnauthorizedError
from flask_utils.errors import WebServerIsDownError
from flask_utils.errors import FailedDependencyError
from flask_utils.errors import ServiceUnavailableError
from flask_utils.errors import OriginIsUnreachableError
from flask_utils.errors import UnprocessableEntityError


class TestGenerateErrorDict:
    @pytest.mark.parametrize(
        "error",
        [
            ConflictError("This is the message", "This is the solution"),
            GoneError("This is the message", "This is the solution"),
            ForbiddenError("This is the message", "This is the solution"),
            UnauthorizedError("This is the message", "This is the solution"),
            NotFoundError("This is the message", "This is the solution"),
            BadRequestError("This is the message", "This is the solution"),
            UnprocessableEntityError("This is the message", "This is the solution"),
            FailedDependencyError("This is the message", "This is the solution"),
            ServiceUnavailableError("This is the message", "This is the solution"),
            OriginIsUnreachableError("This is the message", "This is the solution"),
            WebServerIsDownError("This is the message", "This is the solution"),
            MethodNotAllowedError("This is the message", "This is the solution"),
        ],
    )
    def test_generate_error_dict(self, error):
        from flask_utils.errors._error_template import _generate_error_dict

        assert _generate_error_dict(error) == {
            "success": False,
            "error": {
                "type": error.__class__.__name__,
                "name": error.name,
                "message": error.msg,
                "solution": error.solution,
            },
            "code": error.status_code,
        }
