import inspect
import warnings
from typing import Any
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

# TODO: Allow to set this value from the config/env
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


def _is_allow_empty(value: Any, type_hint: Type) -> bool:  # type: ignore
    """Determine if the value is considered empty and whether it's allowed.

    :param value: Value to check.
    :type value: Any
    :param type_hint: Type hint to check against.
    :type type_hint: Type

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
    if not value:
        # Check if type is explicitly Optional or allow_empty is True
        if _is_optional(type_hint):
            return True
    return False


def _check_type(value: Any, expected_type: Type, curr_depth: int = 0) -> bool:  # type: ignore
    """Check if the value matches the expected type, recursively if necessary.

    :param value: Value to check.
    :type value: Any
    :param expected_type: Expected type.
    :type expected_type: Type
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
        warnings.warn(f"Maximum depth of {VALIDATE_PARAMS_MAX_DEPTH} reached.", SyntaxWarning, stacklevel=2)
        return True
    if expected_type is Any or _is_allow_empty(value, expected_type):  # type: ignore
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
        return any(_check_type(value, arg, (curr_depth + 1)) for arg in args)
    elif origin is list:
        return isinstance(value, list) and all(_check_type(item, args[0], (curr_depth + 1)) for item in value)
    elif origin is dict:
        key_type, val_type = args
        if not isinstance(value, dict):
            return False
        for k, v in value.items():
            if not isinstance(k, key_type):
                return False
            if not _check_type(v, val_type, (curr_depth + 1)):
                return False
        return True
    else:
        return isinstance(value, expected_type)


def validate_params() -> Callable:  # type: ignore
    """
    Decorator to validate request JSON body parameters.

    This decorator ensures that the JSON body of a request matches the specified
    parameter types and includes all required parameters.

    :raises BadRequestError: If the JSON body is malformed,
        the Content-Type header is missing or incorrect, required parameters are missing,
        or parameters are of the wrong type.

    :Example:

    .. code-block:: python

        from flask import Flask, request
        from typing import List, Dict
        from flask_utils.decorators import validate_params
        from flask_utils.errors import BadRequestError

        app = Flask(__name__)

        @app.route("/example", methods=["POST"])
        @validate_params()
        def example(name: str, age: int, is_student: bool, courses: List[str], grades: Dict[str, int]):
            \"""
            This route expects a JSON body with the following:
                - name: str
                - age: int (optional)
                - is_student: bool
                - courses: list of str
                - grades: dict with str keys and int values
            \"""
            # Use the data in your route
            ...

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

    .. warning::
        If a parameter exists both in the route parameters and in the JSON body,
        the value from the JSON body will override the route parameter. A warning
        is issued when this occurs.

        :Example:

        .. code-block:: python

            from flask import Flask, request
            from typing import List, Dict
            from flask_utils.decorators import validate_params
            from flask_utils.errors import BadRequestError

            app = Flask(__name__)

            @app.route("/users/<int:user_id>", methods=["POST"])
            @validate_params()
            def create_user(user_id: int):
                print(f"User ID: {user_id}")
                return "User created"

            ...

            requests.post("/users/123", json={"user_id": 456})
            # Output: User ID: 456

    .. versionchanged:: 1.0.0
        The decorator doesn't take any parameters anymore,
        it loads the types and parameters from the function signature as well as the Flask route's slug parameters.

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
            if not isinstance(data, dict):
                return _handle_bad_request(
                    use_error_handlers,
                    "JSON body must be a dict",
                    original_exception=BadRequestError("JSON body must be a dict"),
                )

            signature = inspect.signature(fn)
            parameters = signature.parameters
            # Extract the parameter names and annotations
            expected_params = {}
            for name, param in parameters.items():
                if param.annotation != inspect.Parameter.empty:
                    expected_params[name] = param.annotation
                else:
                    warnings.warn(f"Parameter {name} has no type annotation.", SyntaxWarning, stacklevel=2)
                    expected_params[name] = Any

            request_data = request.view_args  # Flask route parameters
            for key in data:
                if key in request_data:
                    warnings.warn(
                        f"Parameter {key} is defined in both the route and the JSON body. "
                        f"The JSON body will override the route parameter.",
                        SyntaxWarning,
                        stacklevel=2,
                    )
            request_data.update(data or {})

            for key, type_hint in expected_params.items():
                # TODO: Handle deeply nested types
                if key not in request_data and not _is_optional(type_hint):
                    return _handle_bad_request(
                        use_error_handlers, f"Missing key: {key}", f"Expected keys are: {list(expected_params.keys())}"
                    )

            for key in request_data:
                if key not in expected_params:
                    return _handle_bad_request(
                        use_error_handlers,
                        f"Unexpected key: {key}.",
                        f"Expected keys are: {list(expected_params.keys())}",
                    )

            for key, value in request_data.items():
                if key in expected_params and not _check_type(value, expected_params[key]):
                    return _handle_bad_request(
                        use_error_handlers,
                        f"Wrong type for key {key}.",
                        f"It should be {getattr(expected_params[key], '__name__', str(expected_params[key]))}",
                    )

            provided_values = {}
            for key in expected_params:
                if not _is_optional(expected_params[key]):
                    provided_values[key] = request_data[key]
                else:
                    provided_values[key] = request_data.get(key, None)

            kwargs.update(provided_values)

            return fn(*args, **kwargs)

        return wrapper

    return decorator
