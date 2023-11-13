# backend/app/__init__.py
from flask import Flask

from backend.app.config import Config
from backend.app.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .api.user_routes import api_blueprint
    from .api.direction_routes import api_blueprint
    from .api.log_routes import api_blueprint
    from .api.specialty_routes import api_blueprint
    from .api.session_routes import api_blueprint

    app.register_blueprint(api_blueprint, url_prefix='/')

    with app.app_context():
        db.create_all()  # Создает таблицы

    return app
