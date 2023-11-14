# educationapp/app/services/auth_service.py
from flask_login import LoginManager, login_user
from werkzeug.security import check_password_hash

from educationapp.app.models.user import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def init_auth(app):
    login_manager.login_view = 'user.login'
    login_manager.init_app(app)

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)  # Теперь `login_user` вызывается здесь
        return user
    else:
        return None
