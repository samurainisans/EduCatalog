from flask import Blueprint, render_template, abort, url_for
from flask import jsonify, request
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from educationapp.app import db
from educationapp.app.models.profession import Profession

profession_blueprint = Blueprint('profession', __name__)


@profession_blueprint.route('/professions', methods=['GET'])
def get_professions():
    professions = Profession.query.all()
    return render_template('professions.html', professions=professions)


@profession_blueprint.route('/professions', methods=['POST'])
def add_profession():
    name = request.form.get('name')

    if not name:
        return jsonify({'error': 'No name provided'}), 400

    existing_profession = Profession.query.filter_by(name=name).first()
    if existing_profession:
        return jsonify({'error': 'Profession already exists'}), 409

    new_profession = Profession(name=name)
    db.session.add(new_profession)
    db.session.commit()

    return render_template('professions.html', professions=Profession.query.all())



@profession_blueprint.route('/professions/<int:id>', methods=['DELETE'])
def delete_profession(id):
    profession = Profession.query.get(id)
    if not profession:
        return jsonify({'error': 'Profession not found'}), 404

    db.session.delete(profession)
    db.session.commit()

    return jsonify({'message': 'Profession deleted'}), 200
