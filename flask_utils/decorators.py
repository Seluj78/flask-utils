from typing import Any
from typing import Dict
from typing import Type
from typing import Union
from typing import Callable
from typing import Optional
from typing import get_args
from typing import get_origin
from functools import wraps

from flask import Response
from flask import jsonify
from flask import request
from flask import current_app
from flask import make_response
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import UnsupportedMediaType

from flask_utils.errors import BadRequestError

VALIDATE_PARAMS_MAX_DEPTH = 4


def _handle_bad_request(
    use_error_handlers: bool,
    message: str,
    solution: Optional[str] = None,
    status_code: int = 400,
    original_exception: Optional[Exception] = None,
) -> Response:
    if use_error_handlers:
        raise BadRequestError(message, solution) from original_exception
    else:
        error_response = {"error": message}
        if solution:
            error_response["solution"] = solution
        return make_response(jsonify(error_response), status_code)


def _is_optional(type_hint: Type) -> bool:  # type: ignore
    """Check if the type hint is :data:`~typing.Optional`.

    :param type_hint: Type hint to check.
    :type type_hint: Type

    :return: True if the type hint is :data:`~typing.Optional`, False otherwise.
    :rtype: bool

    :Example:

    .. code-block:: python

        from typing import Optional
        from flask_utils.decorators import _is_optional

        _is_optional(Optional[str])  # True
        _is_optional(str)  # False

    .. versionadded:: 0.2.0
    """
    return get_origin(type_hint) is Union and type(None) in get_args(type_hint)


def _make_optional(type_hint: Type) -> Type:  # type: ignore
    """Wrap type hint with :data:`~typing.Optional` if it's not already.

    :param type_hint: Type hint to wrap.
    :type type_hint: Type

    :return: Type hint wrapped with :data:`~typing.Optional`.
    :rtype: Type

    :Example:

    .. code-block:: python

            from typing import Optional
            from flask_utils.decorators import _make_optional

            _make_optional(str)  # Optional[str]
            _make_optional(Optional[str])  # Optional[str]

    .. versionadded:: 0.2.0
    """
    if not _is_optional(type_hint):
        return Optional[type_hint]  # type: ignore
    return type_hint


def _is_allow_empty(value: Any, type_hint: Type, allow_empty: bool) -> bool:  # type: ignore
    """Determine if the value is considered empty and whether it's allowed.

    :param value: Value to check.
    :type value: Any
    :param type_hint: Type hint to check against.
    :type type_hint: Type
    :param allow_empty: Whether to allow empty values.
    :type allow_empty: bool

    :return: True if the value is empty and allowed, False otherwise.
    :rtype: bool

    :Example:

    .. code-block:: python

            from typing import Optional
            from flask_utils.decorators import _is_allow_empty

            _is_allow_empty(None, str, False)  # False
            _is_allow_empty("", str, False)  # False
            _is_allow_empty(None, Optional[str], False)  # True
            _is_allow_empty("", Optional[str], False)  # True
            _is_allow_empty("", Optional[str], True)  # True
            _is_allow_empty("", str, True)  # True
            _is_allow_empty([], Optional[list], False)  # True

    .. versionadded:: 0.2.0
    """
    if value in [None, "", [], {}]:
        # Check if type is explicitly Optional or allow_empty is True
        if _is_optional(type_hint) or allow_empty:
            return True
    return False


def _check_type(value: Any, expected_type: Type, allow_empty: bool = False, curr_depth: int = 0) -> bool:  # type: ignore
    """Check if the value matches the expected type, recursively if necessary.

    :param value: Value to check.
    :type value: Any
    :param expected_type: Expected type.
    :type expected_type: Type
    :param allow_empty: Whether to allow empty values.
    :type allow_empty: bool
    :param curr_depth: Current depth of the recursive check.
    :type curr_depth: int

    :return: True if the value matches the expected type, False otherwise.
    :rtype: bool

    :Example:

    .. code-block:: python

                from typing import List, Dict
                from flask_utils.decorators import _check_type

                _check_type("hello", str)  # True
                _check_type(42, int)  # True
                _check_type(42.0, float)  # True
                _check_type(True, bool)  # True
                _check_type(["hello", "world"], List[str])  # True
                _check_type({"name": "Jules", "city": "Rouen"}, Dict[str, str])  # True

    It also works recursively:

    .. code-block:: python

                    from typing import List, Dict
                    from flask_utils.decorators import _check_type

                    _check_type(["hello", "world"], List[str])  # True
                    _check_type(["hello", 42], List[str])  # False
                    _check_type([{"name": "Jules", "city": "Rouen"},
                        {"name": "John", "city": "Paris"}], List[Dict[str, str]])  # True
                    _check_type([{"name": "Jules", "city": "Rouen"},
                        {"name": "John", "city": 42}], List[Dict[str, str]])  # False

    .. versionadded:: 0.2.0
    """

    if curr_depth >= VALIDATE_PARAMS_MAX_DEPTH:
        return True
    if expected_type is Any or _is_allow_empty(value, expected_type, allow_empty):  # type: ignore
        return True

    if isinstance(value, bool):
        if expected_type is bool or expected_type is Optional[bool]:  # type: ignore
            return True
        if get_origin(expected_type) is Union:
            return any(arg is bool for arg in get_args(expected_type))
        return False

    origin = get_origin(expected_type)
    args = get_args(expected_type)

    if origin is Union:
        return any(_check_type(value, arg, allow_empty, (curr_depth + 1)) for arg in args)
    elif origin is list:
        return isinstance(value, list) and all(
            _check_type(item, args[0], allow_empty, (curr_depth + 1)) for item in value
        )
    elif origin is dict:
        key_type, val_type = args
        if not isinstance(value, dict):
            return False
        for k, v in value.items():
            if not isinstance(k, key_type):
                return False
            if not _check_type(v, val_type, allow_empty, (curr_depth + 1)):
                return False
        return True
    else:
        return isinstance(value, expected_type)


def validate_params(
    parameters: Dict[Any, Any],
    allow_empty: bool = False,
) -> Callable:  # type: ignore
    """
    Decorator to validate request JSON body parameters.

    This decorator ensures that the JSON body of a request matches the specified
    parameter types and includes all required parameters.

    :param parameters: Dictionary of parameters to validate. The keys are parameter names
                       and the values are the expected types.
    :type parameters: Dict[Any, Any]
    :param allow_empty: Allow empty values for parameters. Defaults to False.
    :type allow_empty: bool

    :raises BadRequestError: If the JSON body is malformed,
        the Content-Type header is missing or incorrect, required parameters are missing,
        or parameters are of the wrong type.

    :Example:

    .. code-block:: python

        from flask import Flask, request
        from typing import List, Dict
        from flask_utils.decorators import validate_params
        from flask_utils.errors.badrequest import BadRequestError

        app = Flask(__name__)

        @app.route("/example", methods=["POST"])
        @validate_params(
            {
                "name": str,
                "age": int,
                "is_student": bool,
                "courses": List[str],
                "grades": Dict[str, int],
            }
        )
        def example():
            \"""
            This route expects a JSON body with the following:
                - name: str
                - age: int (optional)
                - is_student: bool
                - courses: list of str
                - grades: dict with str keys and int values
            \"""
            data = request.get_json()
            return data

    .. tip::
        You can use any of the following types:
            * str
            * int
            * float
            * bool
            * List
            * Dict
            * Any
            * Optional
            * Union

    .. versionchanged:: 0.7.0
        The decorator will now use the custom error handlers if ``register_error_handlers`` has been set to ``True``
        when initializing the :class:`~flask_utils.extension.FlaskUtils` extension.

    .. versionadded:: 0.2.0
    """

    def decorator(fn):  # type: ignore
        @wraps(fn)
        def wrapper(*args, **kwargs):  # type: ignore
            use_error_handlers = (
                current_app.extensions.get("flask_utils") is not None
                and current_app.extensions["flask_utils"].has_error_handlers_registered
            )

            try:
                data = request.get_json()
            except BadRequest as e:
                return _handle_bad_request(use_error_handlers, "The Json Body is malformed.", original_exception=e)
            except UnsupportedMediaType as e:
                return _handle_bad_request(
                    use_error_handlers,
                    "The Content-Type header is missing or is not set to application/json, "
                    "or the JSON body is missing.",
                    original_exception=e,
                )

            if not data:
                return _handle_bad_request(use_error_handlers, "Missing json body.")

            if not isinstance(data, dict):
                return _handle_bad_request(use_error_handlers, "JSON body must be a dict")

            for key, type_hint in parameters.items():
                if not _is_optional(type_hint) and key not in data:
                    return _handle_bad_request(
                        use_error_handlers, f"Missing key: {key}", f"Expected keys are: {list(parameters.keys())}"
                    )

            for key in data:
                if key not in parameters:
                    return _handle_bad_request(
                        use_error_handlers, f"Unexpected key: {key}.", f"Expected keys are: {list(parameters.keys())}"
                    )

            for key in data:
                if key in parameters and not _check_type(data[key], parameters[key], allow_empty):
                    return _handle_bad_request(
                        use_error_handlers,
                        f"Wrong type for key {key}.",
                        f"It should be {getattr(parameters[key], '__name__', str(parameters[key]))}",
                    )

            return fn(*args, **kwargs)

        return wrapper

    return decorator
