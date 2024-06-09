from flask_utils.errors.base_class import BaseFlaskException


class ServiceUnavailableError(BaseFlaskException):
    """
    This is the ServiceUnavailable class for the Exception.
    """

    def __init__(self, msg: str, solution: str = "Try again later.") -> None:
        self.name = "Service Unavailable"
        self.msg = msg
        self.solution = solution
        self.status_code = 503
