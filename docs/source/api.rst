API
===

.. module:: flask_utils
    :synopsis: Flask utilities

This part of the documentation covers all the interfaces of Flask-Utils

Extension
---------

.. automodule:: flask_utils.extension
    :members:

Custom exceptions
-----------------

.. warning:: For any of these errors to work, you need to register the error handlers in your Flask app.

    To do this, you need to pass :attr:`register_error_handlers=True` to the :class:`FlaskUtils` class or to :meth:`~FlaskUtils.init_app()`.

    .. code-block:: python
        
        from flask import Flask
        from flask_utils import FlaskUtils
        
        app = Flask(__name__)
        utils = FlaskUtils(app, register_error_handlers=True)

        # OR

        utils = FlaskUtils()
        utils.init_app(app, register_error_handlers=True)

.. automodule:: flask_utils.errors
     :members:


Decorators
----------

.. automodule:: flask_utils.decorators
    :members:

Utilities
---------

.. automodule:: flask_utils.utils
    :members:

Private API
----------------------

.. autofunction:: flask_utils.decorators._is_optional
.. autofunction:: flask_utils.decorators._make_optional
.. autofunction:: flask_utils.decorators._is_allow_empty
.. autofunction:: flask_utils.decorators._check_type

.. autofunction:: flask_utils.errors._error_template._generate_error_json

.. autofunction:: flask_utils.errors._register_error_handlers
