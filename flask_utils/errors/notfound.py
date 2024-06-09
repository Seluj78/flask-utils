from flask_utils.errors.base_class import BaseFlaskException


class NotFoundError(BaseFlaskException):
    """
    This is the NotFoundError class for the Exception.
    """

    def __init__(self, msg: str, solution: str = "Try again.") -> None:
        self.name = "Not Found"
        self.msg = msg
        self.solution = solution
        self.status_code = 404
