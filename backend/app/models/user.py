# backend/app/models/user.py
from werkzeug.security import generate_password_hash, check_password_hash
from backend.app.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Методы для установки и проверки пароля
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Представление объекта в виде строки
    def __repr__(self):
        return f'<User {self.username}>'
