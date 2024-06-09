from flask_utils.errors.base_class import BaseFlaskException


class FailedDependencyError(BaseFlaskException):
    """
    This is the FailedDependencyError class for the Exception.
    """

    def __init__(self, msg: str, solution: str = "Try again later.") -> None:
        self.name = "Failed Dependency"
        self.msg = msg
        self.solution = solution
        self.status_code = 424
