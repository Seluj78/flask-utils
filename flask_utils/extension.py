from typing import Optional

from flask import Flask

from flask_utils.errors import _register_error_handlers


class FlaskUtils(object):
    """
    FlaskUtils extension class.

    This class currently optionally register the custom error handlers found in :mod:`flask_utils.errors`.
    Call :meth:`init_app` to configure the extension on an application.

    :param app: Flask application instance.
    :param register_error_handlers: Register the custom error handlers. Default is True.

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

    def __init__(self, app: Optional[Flask] = None, register_error_handlers: bool = True):
        if app is not None:
            self.init_app(app, register_error_handlers)

    def init_app(self, app: Flask, register_error_handlers: bool = True) -> None:
        """Initialize a Flask application for use with this extension instance. This
        must be called before any request is handled by the application.

        If the app is created with the factory pattern, this should be called after the app
        is created to configure the extension.

        If `register_error_handlers` is True, the custom error handlers will be registered and
        can then be used in routes to raise errors.

        :param app: The Flask application to initialize.
        :param register_error_handlers: Register the custom error handlers. Default is True.

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

        app.extensions["flask_utils"] = self
