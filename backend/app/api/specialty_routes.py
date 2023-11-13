from flask import jsonify, request
from backend.app.database import db

from backend.app.api.user_routes import api_blueprint
from backend.app.models.specialty import Specialty


@api_blueprint.route('/specialties', methods=['GET'])
def get_specialties():
    specialties = Specialty.query.all()
    return jsonify([specialty.to_dict() for specialty in specialties])

# Получение информации о специальности
@api_blueprint.route('/specialties/<int:specialty_id>', methods=['GET'])
def get_specialty(specialty_id):
    specialty = Specialty.query.get(specialty_id)
    if specialty:
        return jsonify(specialty.to_dict())
    return jsonify({'message': 'Specialty not found'}), 404

# Создание новой специальности
@api_blueprint.route('/specialties', methods=['POST'])
def create_specialty():
    data = request.json
    name = data.get('name')
    cut_off_score = data.get('cut_off_score')

    if not name or cut_off_score is None:
        return jsonify({'message': 'Missing name or cut_off_score'}), 400

    new_specialty = Specialty(name=name, cut_off_score=cut_off_score)
    db.session.add(new_specialty)
    db.session.commit()

    return jsonify({'message': 'Specialty created'}), 201
