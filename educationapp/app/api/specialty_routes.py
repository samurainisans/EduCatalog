from flask import jsonify, request, Blueprint, render_template, url_for
from werkzeug.utils import redirect

from educationapp.app.database import db

from educationapp.app.models.specialty import Specialty

specialty_blueprint = Blueprint('specialty', __name__)


@specialty_blueprint.route('/specialties')
def get_specialties():
    specialties = Specialty.query.all()
    return render_template('specialties.html', specialties=specialties)


# Получение информации о специальности
@specialty_blueprint.route('/specialties/<int:specialty_id>', methods=['GET'])
def get_specialty(specialty_id):
    specialty = Specialty.query.get(specialty_id)
    if specialty:
        return jsonify(specialty.to_dict())
    return jsonify({'message': 'Specialty not found'}), 404


# Создание новой специальности
@specialty_blueprint.route('/specialties', methods=['POST'])
def create_specialty():
    name = request.form.get('name')
    cut_off_score = request.form.get('cut_off_score')

    if not name or not cut_off_score:
        return jsonify({'error': 'Некорректные данные'}), 400

    if Specialty.query.filter_by(name=name).first():
        return jsonify({'error': 'Специальность уже существует'}), 409

    new_specialty = Specialty(name=name, cut_off_score=cut_off_score)
    db.session.add(new_specialty)
    db.session.commit()
    return redirect(url_for('specialty.get_specialties'))


