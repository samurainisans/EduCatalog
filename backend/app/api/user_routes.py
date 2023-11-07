from flask import Blueprint

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/login', methods=['POST'])
def login():
    # Логика входа пользователя
    pass
