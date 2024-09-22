def is_it_true(value: str) -> bool:
    """
    This function checks if a string value is true.
    Useful for flask's request.form.get() method and request.args.get() method

    :param value: String value to check if it is true
    :type value: str

    :return: True if value is true, False otherwise
    :rtype: bool

    :Example:

    .. code-block:: python

        from flask_utils import is_it_true

        @app.route('/example', methods=['GET'])
        def example():
            is_ordered = request.args.get('is_ordered', type=is_it_true, default=False)

    This allows your API to accept these kind of requests:

    .. code-block:: python

        import requests

        response = requests.get('http://localhost:5000/example?is_ordered=true')
        print(response.json())  # True

        response = requests.get('http://localhost:5000/example?is_ordered=1')
        print(response.json())  # True

        response = requests.get('http://localhost:5000/example?is_ordered=yes')
        print(response.json())  # True

    .. versionadded:: 0.4.0
    """
    return value.lower() in ("true", "1", "yes")
