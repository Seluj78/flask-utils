from flask import Flask

from flask_utils import FlaskUtils
from flask_utils import BadRequestError


class TestExtension:
    def test_init_app(self):
        app = Flask(__name__)
        assert "flask_utils" not in app.extensions
        fu = FlaskUtils()

        fu.init_app(app)
        assert "flask_utils" in app.extensions

    def test_normal_instantiation(self):
        app = Flask(__name__)

        assert "flask_utils" not in app.extensions

        FlaskUtils(app)

        assert "flask_utils" in app.extensions

    def test_error_handlers_not_registered(self):
        app = Flask(__name__)

        FlaskUtils(app, register_error_handlers=False)

        @app.route("/")
        def index():
            raise BadRequestError("Bad Request")

        with app.test_client() as client:
            response = client.get("/")
            assert response.status_code == 500

    def test_error_handlers_registered(self):
        app = Flask(__name__)

        FlaskUtils(app, register_error_handlers=True)

        @app.route("/")
        def index():
            raise BadRequestError("Bad Request")

        with app.test_client() as client:
            response = client.get("/")
            assert response.status_code == 400
