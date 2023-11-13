from flask import jsonify, request
from backend import app
from backend.app.database import db

from backend.app.api.user_routes import api_blueprint
from backend.app.models.session import Session


# Получение списка всех сессий
@api_blueprint.route('/sessions', methods=['GET'])
def get_sessions():
    sessions = Session.query.all()
    return jsonify([session.to_dict() for session in sessions])

# Получение информации о сессии
@api_blueprint.route('/sessions/<int:session_id>', methods=['GET'])
def get_session(session_id):
    session = Session.query.get(session_id)
    if session:
        return jsonify(session.to_dict())
    return jsonify({'message': 'Session not found'}), 404

# Создание новой сессии
@api_blueprint.route('/sessions', methods=['POST'])
def create_session():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'message': 'Missing user_id'}), 400

    new_session = Session(user_id=user_id)
    db.session.add(new_session)
    db.session.commit()

    return jsonify({'message': 'Session created'}), 201
