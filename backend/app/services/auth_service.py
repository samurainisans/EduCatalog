# backend/app/services/auth_service.py
from backend.app.models.user import User
from werkzeug.security import check_password_hash
from flask import session


def authenticate_user(username, password):
    """
    Функция для аутентификации пользователя.
    Проверяет соответствие предоставленного имени пользователя и пароля с данными в базе данных.
    Возвращает пользователя при успешной аутентификации, иначе None.
    """
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        # Устанавливаем ID пользователя в сессию
        session['user_id'] = user.id
        return user
    else:
        return None


def logout_user():
    """
    Функция для выхода пользователя.
    Удаляет ID пользователя из сессии.
    """
    session.pop('user_id', None)
