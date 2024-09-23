from typing import Optional


class _BaseFlaskException(Exception):
    """
    This is the base class for all the exceptions in this package.

    :param name: The name of the error
    :type name: str

    :param msg: The message to be displayed
    :type msg: str

    :param solution: The solution to the problem
    :type solution: str

    :param status_code: The status code to be returned
    :type status_code: int

    :Example:

    .. code-block:: python

        from flask_utils.errors import _BaseFlaskException

        class MyError(_BaseFlaskException):
            self.name = "MyError"
            self.msg = msg
            self.solution = solution
            self.status_code = 666

    .. versionadded:: 0.1.0
    """

    name: str = "BaseError"
    msg: str = "An error occurred"
    solution: Optional[str] = "Try again."
    status_code: int = 400
