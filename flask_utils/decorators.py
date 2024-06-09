from functools import wraps
from typing import Any
from typing import Dict
from typing import get_args
from typing import get_origin
from typing import Optional
from typing import Type
from typing import Union

from flask import request
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import UnsupportedMediaType

from flask_utils.errors import BadRequestError

# TODO: Turn flask-utils into a class that registers the app (like Flask-Cors for example)
#  and the error handlers optionally, that way we can either use BadRequestError or just return a 400

VALIDATE_PARAMS_MAX_DEPTH = 4


def is_optional(type_hint: Type) -> bool:
    """Check if the type hint is Optional[SomeType]."""
    return get_origin(type_hint) is Union and type(None) in get_args(type_hint)


def make_optional(type_hint: Type) -> Type:
    """Wrap type hint with Optional if it's not already."""
    if not is_optional(type_hint):
        return Optional[type_hint]  # type: ignore
    return type_hint


def is_allow_empty(value: Any, type_hint: Type, allow_empty: bool) -> bool:
    """Determine if the value is considered empty and whether it's allowed."""
    if value in [None, "", [], {}]:
        # Check if type is explicitly Optional or allow_empty is True
        if is_optional(type_hint) or allow_empty:
            return True
    return False


def check_type(value: Any, expected_type: Type, allow_empty: bool = False, curr_depth: int = 0) -> bool:
    if curr_depth >= VALIDATE_PARAMS_MAX_DEPTH:
        return True
    if expected_type is Any or is_allow_empty(value, expected_type, allow_empty):
        return True

    if isinstance(value, bool):
        if expected_type is bool or expected_type is Optional[bool]:
            return True
        if get_origin(expected_type) is Union:
            return any(arg is bool for arg in get_args(expected_type))
        return False

    origin = get_origin(expected_type)
    args = get_args(expected_type)

    if origin is Union:
        return any(check_type(value, arg, allow_empty, (curr_depth + 1)) for arg in args)
    elif origin is list:
        return isinstance(value, list) and all(
            check_type(item, args[0], allow_empty, (curr_depth + 1)) for item in value
        )
    elif origin is dict:
        key_type, val_type = args
        if not isinstance(value, dict):
            return False
        for k, v in value.items():
            if not isinstance(k, key_type):
                return False
            if not check_type(v, val_type, allow_empty, (curr_depth + 1)):
                return False
        return True
    else:
        return isinstance(value, expected_type)


def validate_params(
    parameters: Dict[Any, Any],
    allow_empty: bool = False,
):
    """Decorator to validate request JSON body parameters.

    Args:
        parameters (Dict[Any, Any]): Dictionary of parameters to validate.
        allow_empty (bool, optional): Allow empty values for parameters.
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                data = request.get_json()
            except BadRequest:
                raise BadRequestError("The Json Body is malformed.")
            except UnsupportedMediaType:
                raise BadRequestError(
                    "The Content-Type header is missing or is not set to application/json, or the JSON body is missing."
                )

            if not data:
                raise BadRequestError("Missing json body.")

            if not isinstance(data, dict):
                raise BadRequestError("JSON body must be a dict")

            for key, type_hint in parameters.items():
                if not is_optional(type_hint) and key not in data:
                    raise BadRequestError(f"Missing key: {key}", f"Expected keys are: {parameters.keys()}")

            for key in data:
                if key not in parameters:
                    raise BadRequestError(
                        f"Unexpected key: {key}.",
                        f"Expected keys are: {parameters.keys()}",
                    )

            for key in data:
                if key in parameters and not check_type(data[key], parameters[key], allow_empty):
                    raise BadRequestError(f"Wrong type for key {key}.", f"It should be {parameters[key]}")

            return fn(*args, **kwargs)

        return wrapper

    return decorator
