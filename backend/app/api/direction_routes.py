from flask import jsonify, request

from backend.app.database import db
from backend.app.api.user_routes import api_blueprint
from backend.app.models.direction import Direction


@api_blueprint.route('/directions', methods=['GET'])
def get_directions():
    directions = Direction.query.all()
    return jsonify([direction.to_dict() for direction in directions]), 200


@api_blueprint.route('/directions', methods=['POST'])
def create_direction():
    data = request.get_json()
    new_direction = Direction(title=data['title'], specialty_id=data['specialty_id'])
    db.session.add(new_direction)
    db.session.commit()
    return jsonify(new_direction.to_dict()), 201


@api_blueprint.route('/directions/<int:direction_id>', methods=['PUT'])
def update_direction(direction_id):
    direction = Direction.query.get_or_404(direction_id)
    data = request.get_json()
    direction.title = data['title']
    direction.specialty_id = data['specialty_id']
    db.session.commit()
    return jsonify(direction.to_dict()), 200
