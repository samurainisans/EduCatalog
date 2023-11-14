from flask import jsonify, request, Blueprint, render_template, url_for
from werkzeug.utils import redirect

from educationapp.app.database import db
from educationapp.app.models.profession import Profession

from educationapp.app.models.specialty import Specialty

specialty_blueprint = Blueprint('specialty', __name__)


@specialty_blueprint.route('/specialties')
def get_specialties():
    specialties = Specialty.query.all()
    professions = Profession.query.all()
    return render_template('specialties.html', specialties=specialties, professions=professions)


# Получение информации о специальности
@specialty_blueprint.route('/specialties/<int:specialty_id>', methods=['GET'])
def get_specialty(specialty_id):
    specialty = Specialty.query.get(specialty_id)
    if specialty:
        return jsonify(specialty.to_dict())
    return jsonify({'message': 'Specialty not found'}), 404


@specialty_blueprint.route('/specialties', methods=['POST'])
def create_specialty():
    name = request.form['name']
    code = request.form['code']
    profession_id = request.form['profession_id']
    education_program = request.form['education_program']
    education_level = request.form['education_level']
    form_of_education = request.form['form_of_education']
    standard_education_duration = request.form['standard_education_duration']
    qualification = request.form['qualification']

    existing_specialty = Specialty.query.filter_by(code=code).first()
    if existing_specialty:
        return jsonify({'message': 'Specialty code already exists'}), 400

    existing_specialty = Specialty.query.filter_by(name=name).first()
    if existing_specialty:
        return jsonify({'message': 'Specialty name already exists'}), 400

    if not all([name, code, profession_id, education_program, education_level, form_of_education,
                standard_education_duration, qualification]):
        return jsonify({'message': 'Missing data'}), 400

    new_specialty = Specialty(name=name, code=code, profession_id=profession_id, education_program=education_program,
                              education_level=education_level, form_of_education=form_of_education,
                              standard_education_duration=standard_education_duration, qualification=qualification)
    db.session.add(new_specialty)
    db.session.commit()

    return redirect(url_for('specialty.get_specialties'))
