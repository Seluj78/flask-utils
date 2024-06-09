from flask_utils.errors.base_class import BaseFlaskException


class UnauthorizedError(BaseFlaskException):
    """
    This is the UnauthorizedError class for the Exception.
    """

    def __init__(self, msg: str, solution: str = "Try again.") -> None:
        self.name = "Unauthorized"
        self.msg = msg
        self.solution = solution
        self.status_code = 401
