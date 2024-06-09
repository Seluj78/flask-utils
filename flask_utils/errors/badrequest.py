from flask_utils.errors.base_class import BaseFlaskException


class BadRequestError(BaseFlaskException):
    """
    This is the BadRequestError class for the Exception.
    """

    def __init__(self, msg: str, solution: str = "Try again.") -> None:
        self.name = "Bad Request"
        self.msg = msg
        self.solution = solution
        self.status_code = 400
