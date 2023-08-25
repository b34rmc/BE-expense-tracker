from flask import request, Response, Blueprint

import controllers

category = Blueprint('category', __name__)

@category.route('/category', methods=['POST'])
def add_category() -> Response:
    return controllers.add_category(request)

@category.route('/categories', methods=['GET'])
def get_categories() -> Response:
    return controllers.get_categories(request)

@category.route('/category/<category_id>', methods=['GET'])
def get_category(category_id) -> Response:
    return controllers.get_category(request, category_id)

@category.route('/category/<category_id>', methods=['PUT'])
def update_category(category_id) -> Response:
    return controllers.update_category(request, category_id)

@category.route('/category/<category_id>', methods=['DELETE'])
def delete_category(category_id) -> Response:
    return controllers.delete_category(request, category_id)

