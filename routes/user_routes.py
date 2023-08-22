from flask import request, Response, Blueprint

import controllers

user = Blueprint('user', __name__)

@user.route('/user', methods=['POST'])
def add_user() -> Response:
    return controllers.add_user(request)


@user.route('/users', methods=['GET'])
def get_users() -> Response:
    return controllers.get_users(request)


@user.route('/user/<user_id>', methods=['GET'])
def get_user() -> Response:
    return controllers.get_user(request)


@user.route('/user/<user_id>', methods=['PUT', 'PATCH'])
def update_user() -> Response:
    return controllers.update_user(request)


@user.route('/user/<user_id>', methods=['DELETE'])
def delete_user() -> Response:
    return controllers.delete_user(request)