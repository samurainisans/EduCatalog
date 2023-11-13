from flask import Blueprint, flash, redirect, url_for, render_template
from backend.app.database import db
from backend.app.models.user import User
from backend.app.services.auth_service import authenticate_user, logout_user

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

api_blueprint = Blueprint('api', __name__)


# Вход пользователя
@api_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Необходимо ввести имя пользователя и пароль', 'warning')
            return render_template('login.html')

        user = authenticate_user(username, password)
        if user:
            # Аутентификация успешна
            flash('Вход выполнен успешно', 'success')
            return render_template('home.html')  # Перенаправляем на защищенный маршрут
        else:
            # Неверное имя пользователя или пароль
            flash('Неверное имя пользователя или пароль', 'danger')
            return render_template('login.html')

    # Если метод GET, показываем страницу входа
    return render_template('login.html')


@api_blueprint.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('Вы успешно вышли из системы', 'success')
    return render_template('login.html')


# Получение списка всех пользователей
@api_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


# Получение информации о пользователе по ID
@api_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({'message': 'User not found'}), 404


# Создание нового пользователя
@api_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Проверяем, существует ли уже пользователь с таким именем
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Пользователь с таким именем уже существует', 'danger')
        else:
            # Хешируем пароль перед сохранением в базу данных
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password_hash=hashed_password)

            db.session.add(new_user)
            db.session.commit()

            flash('Регистрация успешно завершена', 'success')
            return redirect(url_for('login'))  # Перенаправляем пользователя на страницу авторизации

    return render_template('register.html')


# Обновление пользователя
@api_blueprint.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.json
    user.username = data.get('username', user.username)
    password = data.get('password')
    if password:
        user.password_hash = generate_password_hash(password)

    db.session.commit()

    return jsonify({'message': 'User updated'}), 200
