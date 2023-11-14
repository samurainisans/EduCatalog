from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user, current_user

from educationapp.app.database import db
from educationapp.app.models.log import LogEntry
from educationapp.app.models.session import Session
from educationapp.app.models.user import User, Role

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from educationapp.app.services.auth_service import authenticate_user

app = Flask(__name__)

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/', methods=['GET'])
def home():
    return render_template('home.html')


# Вход пользователя
@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Необходимо ввести имя пользователя и пароль', 'warning')
            return render_template('login.html')

        user = authenticate_user(username, password)
        if user:
            # `login_user` вызывается внутри `authenticate_user`
            flash('Вход выполнен успешно', 'success')

            # Создаем новую запись в журнале
            new_log_entry = LogEntry(user_id=current_user.id, action='login')
            db.session.add(new_log_entry)

            # Создаем новую сессию
            new_session = Session(user_id=current_user.id)
            db.session.add(new_session)

            db.session.commit()

            return redirect(url_for('user.home'))  # Убедитесь, что у вас есть endpoint для 'home'
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
            return render_template('login.html')

    # Если метод GET, показываем страницу входа
    return render_template('login.html')



@user_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user.is_authenticated:  # Проверяем, вошел ли пользователь в систему
        # Создаем новую запись в журнале
        new_log_entry = LogEntry(user_id=current_user.id, action='logout')
        db.session.add(new_log_entry)

        # Закрываем текущую сессию
        current_session = Session.query.filter_by(user_id=current_user.id).order_by(Session.timestamp.desc()).first()
        if current_session:
            db.session.delete(current_session)

        db.session.commit()

    logout_user()
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('user.login'))  # Перенаправляем на страницу входа



# Получение списка всех пользователей
@user_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


# Получение информации о пользователе по ID
@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({'message': 'User not found'}), 404


# Создание нового пользователя
@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Пользователь с таким именем уже существует', 'danger')
            return render_template('register.html')

        # Хешируем пароль перед сохранением в базу данных
        hashed_password = generate_password_hash(password)

        # Здесь мы находим роль по умолчанию, которую хотим назначить новым пользователям
        # Убедитесь, что эта роль существует в базе данных
        default_role = Role.query.filter_by(name='User').first()
        if not default_role:
            # Если роль по умолчанию не найдена, создаем ее
            default_role = Role(name='User')
            db.session.add(default_role)
            db.session.commit()

        # Создаем нового пользователя с ролью по умолчанию
        new_user = User(username=username, password_hash=hashed_password, role=default_role)

        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация успешно завершена', 'success')
        return redirect(url_for('user.login'))

    return render_template('register.html')


# Обновление пользователя
@user_blueprint.route('/users/<int:user_id>', methods=['PUT'])
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
