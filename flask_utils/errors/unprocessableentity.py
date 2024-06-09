from flask_utils.errors.base_class import BaseFlaskException


class UnprocessableEntityError(BaseFlaskException):
    """
    This is the UnprocessableEntityError class for the Exception.
    """

    def __init__(self, msg: str, solution: str = "Try again.") -> None:
        self.name = "Unprocessable Entity"
        self.msg = msg
        self.solution = solution
        self.status_code = 422
