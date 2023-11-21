from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user, current_user

from educationapp.app.database import db
from educationapp.app.models.direction import Direction
from educationapp.app.models.log import LogEntry
from educationapp.app.models.profession import Profession
from educationapp.app.models.session import Session
from educationapp.app.models.specialty import Specialty
from educationapp.app.models.user import User, Role

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from educationapp.app.services.auth_service import authenticate_user

app = Flask(__name__)

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/', methods=['GET'])
def home():
    return render_template('home.html')


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
            flash('Вход выполнен успешно', 'success')

            new_log_entry = LogEntry(user_id=current_user.id, action='login')
            db.session.add(new_log_entry)

            new_session = Session(user_id=current_user.id)
            db.session.add(new_session)

            db.session.commit()

            return redirect(url_for('user.home'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
            return render_template('login.html')

    return render_template('login.html')


@app.before_request
def log_user_action():
    if current_user.is_authenticated:
        new_session = Session(user_id=current_user.id)
        db.session.add(new_session)
        db.session.commit()


@user_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user.is_authenticated:
        new_log_entry = LogEntry(user_id=current_user.id, action='logout')
        db.session.add(new_log_entry)

        current_session = Session.query.filter_by(user_id=current_user.id).order_by(Session.timestamp.desc()).first()
        if current_session:
            db.session.delete(current_session)

        db.session.commit()

    logout_user()
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('user.login'))


def combine_data(directions, logs, professions, sessions, specialties):
    combined_data = []

    for direction in directions:
        related_logs = [log for log in logs if log.user_id == direction.specialty_id]
        related_profession = next((prof for prof in professions if prof.id == direction.specialty_id), None)
        related_sessions = [session for session in sessions if session.user_id == direction.specialty_id]
        related_specialty = next((spec for spec in specialties if spec.id == direction.specialty_id), None)

        combined_entry = {
            "direction": direction,
            "related_logs": related_logs,
            "related_profession": related_profession,
            "related_sessions": related_sessions,
            "related_specialty": related_specialty
        }

        combined_data.append(combined_entry)

    return combined_data




@user_blueprint.route('/review')
@login_required
def review():
    if current_user.role.name != 'Manager':
        return redirect(url_for('home.html'))

    # Example queries (to be adjusted based on your actual data relationships)
    directions = Direction.query.all()
    logs = LogEntry.query.all()
    professions = Profession.query.all()
    sessions = Session.query.all()
    specialties = Specialty.query.all()

    # Combine the data in a meaningful way
    combined_data = combine_data(directions, logs, professions, sessions, specialties)

    return render_template('review.html', data=combined_data)


@user_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({'message': 'User not found'}), 404


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Пользователь с таким именем уже существует', 'danger')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)

        default_role = Role.query.filter_by(name='User').first()
        if not default_role:
            default_role = Role(name='User')
            db.session.add(default_role)
            db.session.commit()

        new_user = User(username=username, password_hash=hashed_password, role=default_role)

        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация успешно завершена', 'success')
        return redirect(url_for('user.login'))

    return render_template('register.html')


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
