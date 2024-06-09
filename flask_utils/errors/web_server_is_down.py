from flask_utils.errors.base_class import BaseFlaskException


class WebServerIsDownError(BaseFlaskException):
    """
    This is the WebServerIsDownError class for the Exception.
    """

    def __init__(self, msg: str, solution: str = "Try again later.") -> None:
        self.name = "Web Server Is Down"
        self.msg = msg
        self.solution = solution
        self.status_code = 521
