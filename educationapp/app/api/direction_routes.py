from flask import jsonify, request, Blueprint, render_template, url_for
from werkzeug.utils import redirect

from educationapp.app.database import db
from educationapp.app.models.direction import Direction
from educationapp.app.models.specialty import Specialty

direction_blueprint = Blueprint('direction', __name__)


@direction_blueprint.route('/directions')
def get_directions():
    directions = Direction.query.all()
    specialties = Specialty.query.all()
    return render_template('directions.html', directions=directions, specialties=specialties)


@direction_blueprint.route('/directions', methods=['POST'])
def create_direction():
    title = request.form.get('title')
    specialty_id = request.form.get('specialty_id')

    if not title or not specialty_id:
        return jsonify({'error': 'Некорректные данные'}), 400

    if Direction.query.filter_by(title=title).first():
        return jsonify({'error': 'Направление уже существует'}), 409

    new_direction = Direction(title=title, specialty_id=specialty_id)
    db.session.add(new_direction)
    db.session.commit()
    return redirect(url_for('direction.get_directions'))


@direction_blueprint.route('/directions/<int:direction_id>', methods=['PUT'])
def update_direction(direction_id):
    direction = Direction.query.get_or_404(direction_id)
    data = request.get_json()
    direction.title = data['title']
    direction.specialty_id = data['specialty_id']
    db.session.commit()
    return jsonify(direction.to_dict()), 200
