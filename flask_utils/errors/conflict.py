from flask_utils.errors.base_class import BaseFlaskException


class ConflictError(BaseFlaskException):
    """
    This is the ConflictError class for the Exception.
    """

    def __init__(self, msg: str, solution: str = "Try again.") -> None:
        self.name = "Conflict"
        self.msg = msg
        self.solution = solution
        self.status_code = 409
