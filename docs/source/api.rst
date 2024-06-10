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
    To do this, you can call :meth:`flask_utils.errors.register_error_handlers` with your Flask app as an argument.

    .. code-block:: python

        from flask_utils import register_error_handlers
        register_error_handlers(app)

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
