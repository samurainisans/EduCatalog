from flask import jsonify, request, Blueprint
from educationapp.app.database import db
from educationapp.app.models.log import LogEntry

log_blueprint = Blueprint('log_blueprint', __name__)

@log_blueprint.route('/logs', methods=['GET'])
def get_logs():
    logs = LogEntry.query.all()
    return jsonify([log.to_dict() for log in logs]), 200


@log_blueprint.route('/logs', methods=['POST'])
def create_log():
    data = request.get_json()
    new_log = LogEntry(user_id=data['user_id'], action=data['action'], target=data['target'])
    db.session.add(new_log)
    db.session.commit()
    return jsonify(new_log.to_dict()), 201


@log_blueprint.route('/logs/<int:log_id>', methods=['PUT'])
def update_log(log_id):
    log = LogEntry.query.get_or_404(log_id)
    data = request.get_json()
    log.user_id = data['user_id']
    log.action = data['action']
    log.target = data['target']
    db.session.commit()
    return jsonify(log.to_dict()), 200
