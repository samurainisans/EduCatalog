from flask import jsonify, request, Blueprint
from educationapp import app
from educationapp.app.database import db

from educationapp.app.models.session import Session

session_blueprint = Blueprint('session', __name__)

# Получение списка всех сессий
@session_blueprint.route('/sessions', methods=['GET'])
def get_sessions():
    sessions = Session.query.all()
    return jsonify([session.to_dict() for session in sessions])


# Получение информации о сессии
@session_blueprint.route('/sessions/<int:session_id>', methods=['GET'])
def get_session(session_id):
    session = Session.query.get(session_id)
    if session:
        return jsonify(session.to_dict())
    return jsonify({'message': 'Session not found'}), 404


# Создание новой сессии
@session_blueprint.route('/sessions', methods=['POST'])
def create_session():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'message': 'Missing user_id'}), 400

    new_session = Session(user_id=user_id)
    db.session.add(new_session)
    db.session.commit()

    return jsonify({'message': 'Session created'}), 201
