from typing import Optional


class _BaseFlaskException(Exception):
    """
    This is the base class for all the exceptions in this package.

    :param msg: The message to be displayed in the error.
    :type msg: str
    :param solution: The solution to the error.
    :type solution: Optional[str]
    :param status_code: The status code of the error.
    :type status_code: Optional[int]
    :param name: The name of the error.
    :type name: Optional[str]

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

    name: Optional[str] = None
    msg: Optional[str] = None
    solution: Optional[str] = "Try again."
    status_code: Optional[int] = 400
