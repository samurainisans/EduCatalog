from flask import jsonify, request, Blueprint
from educationapp.app.models.profession import Profession

profession_blueprint = Blueprint('profession', __name__)


@profession_blueprint.route('/professions', methods=['GET'])
def get_professions():
    professions = Profession.query.all()
    return jsonify([profession.to_dict() for profession in professions])


