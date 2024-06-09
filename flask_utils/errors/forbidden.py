from flask_utils.errors.base_class import BaseFlaskException


class ForbiddenError(BaseFlaskException):
    """
    This is the ForbiddenError class for the Exception.
    """

    def __init__(self, msg: str, solution: str = "Try again.") -> None:
        self.name = "Forbidden Error"
        self.msg = msg
        self.solution = solution
        self.status_code = 403
