from typing import Optional

from flask import Flask

from flask_utils.errors import _register_error_handlers


class FlaskUtils(object):
    """
    FlaskUtils extension class.

    This class currently optionally register the custom error handlers found in :mod:`flask_utils.errors`.
    Call :meth:`init_app` to configure the extension on an application.

    :param app: Flask application instance.
    :type app: Optional[Flask]

    :param register_error_handlers: Register the custom error handlers. Default is ``True``.
    :param register_error_handlers: bool

    :Example:

    .. code-block:: python

            from flask import Flask
            from flask_utils import FlaskUtils

            app = Flask(__name__)
            fu = FlaskUtils(app)

            # or

            fu = FlaskUtils()
            fu.init_app(app)

    .. versionchanged:: 1.0.0
        The :func:`~flask_utils.decorators.validate_params` decorator will now use the ``VALIDATE_PARAMS_MAX_DEPTH``
        config variable to determine the maximum depth of the validation for dictionaries.

        :Example:

        .. code-block:: python

            from flask import Flask
            from flask_utils import FlaskUtils

            app = Flask(__name__)
            fu = FlaskUtils(app)
            app.config["VALIDATE_PARAMS_MAX_DEPTH"] = 3

    .. versionadded:: 0.5.0
    """

    def __init__(self, app: Optional[Flask] = None, register_error_handlers: bool = True):
        """
        :param app: Flask application instance.
        :type app: Optional[Flask]

        :param register_error_handlers: Register the custom error handlers. Default is ``True``.
        :type register_error_handlers: bool

        :Example:

        .. code-block:: python

                from flask import Flask
                from flask_utils import FlaskUtils

                app = Flask(__name__)
                fu = FlaskUtils(app)

                # or

                fu = FlaskUtils()
                fu.init_app(app)

        .. versionadded:: 0.5.0
        """
        self.has_error_handlers_registered = False

        if app is not None:
            self.init_app(app, register_error_handlers)

    def init_app(self, app: Flask, register_error_handlers: bool = True) -> None:
        """
        :param app: The Flask application to initialize.
        :type app: Flask

        :param register_error_handlers: Register the custom error handlers. Default is ``True``.
        :type register_error_handlers: bool

        Initialize a Flask application for use with this extension instance. This
        must be called before any request is handled by the application.

        If the app is created with the factory pattern, this should be called after the app
        is created to configure the extension.

        If ``register_error_handlers`` is ``True``, the custom error handlers will be registered and
        can then be used in routes to raise errors. This is enabled by default.
        The decorator :func:`~flask_utils.decorators.validate_params` will also use the custom error handlers
        if set to ``True``.

        .. versionchanged:: 0.7.0
            Setting ``register_error_handlers`` to True will now enable using the custom error handlers
            in the :func:`~flask_utils.decorators.validate_params`. decorator.

        :Example:

        .. code-block:: python

                from flask import Flask
                from flask_utils import FlaskUtils

                app = Flask(__name__)
                fu = FlaskUtils()
                fu.init_app(app)

        .. versionadded:: 0.5.0
        """
        if register_error_handlers:
            _register_error_handlers(app)
            self.has_error_handlers_registered = True

        app.extensions["flask_utils"] = self
        app.config.setdefault("VALIDATE_PARAMS_MAX_DEPTH", 4)
