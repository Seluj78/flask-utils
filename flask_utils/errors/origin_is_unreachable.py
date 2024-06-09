from flask_utils.errors.base_class import BaseFlaskException


class OriginIsUnreachableError(BaseFlaskException):
    """
    This is the OriginIsUnreachableError class for the Exception.
    """

    def __init__(self, msg: str, solution: str = "Try again later.") -> None:
        self.name = "Origin Is Unreachable"
        self.msg = msg
        self.solution = solution
        self.status_code = 523
