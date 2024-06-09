from flask_utils.errors.base_class import BaseFlaskException


class GoneError(BaseFlaskException):
    """
    This is the GoneError class for the Exception.
    """

    def __init__(self, msg: str, solution: str = "Try again later.") -> None:
        self.name = "Ressource is gone."
        self.msg = msg
        self.solution = solution
        self.status_code = 410
