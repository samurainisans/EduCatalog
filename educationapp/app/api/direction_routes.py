from flask import jsonify, request, Blueprint, render_template

from educationapp.app.database import db
from educationapp.app.models.direction import Direction


direction_blueprint = Blueprint('direction', __name__)

@direction_blueprint.route('/directions')
def get_directions():
    directions = Direction.query.all()
    return render_template('directions.html', directions=directions)


@direction_blueprint.route('/directions', methods=['POST'])
def create_direction():
    data = request.get_json()
    new_direction = Direction(title=data['title'], specialty_id=data['specialty_id'])
    db.session.add(new_direction)
    db.session.commit()
    return jsonify(new_direction.to_dict()), 201


@direction_blueprint.route('/directions/<int:direction_id>', methods=['PUT'])
def update_direction(direction_id):
    direction = Direction.query.get_or_404(direction_id)
    data = request.get_json()
    direction.title = data['title']
    direction.specialty_id = data['specialty_id']
    db.session.commit()
    return jsonify(direction.to_dict()), 200
