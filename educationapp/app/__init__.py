from flask import Flask
from educationapp.app.config import Config
from educationapp.app.database import db
from educationapp.app.models import direction, log, session, specialty, user, profession
from educationapp.app.models.user import Role

from educationapp.app.services.auth_service import init_auth


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()
        if Role.query.count() == 0:
            roles = ['Administrator', 'Manager', 'User']
            for role_name in roles:
                role = Role(name=role_name)
                db.session.add(role)
            db.session.commit()

    init_auth(app)

    from educationapp.app.api.direction_routes import direction_blueprint
    from educationapp.app.api.log_routes import log_blueprint
    from educationapp.app.api.session_routes import session_blueprint
    from educationapp.app.api.specialty_routes import specialty_blueprint
    from educationapp.app.api.user_routes import user_blueprint
    from educationapp.app.api.profession_routes import profession_blueprint

    app.register_blueprint(user_blueprint)
    app.register_blueprint(direction_blueprint)
    app.register_blueprint(log_blueprint)
    app.register_blueprint(session_blueprint)
    app.register_blueprint(specialty_blueprint)
    app.register_blueprint(profession_blueprint)

    return app
