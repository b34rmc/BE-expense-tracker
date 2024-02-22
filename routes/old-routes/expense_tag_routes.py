from flask import request, Response, Blueprint

import controllers

tag = Blueprint('tag', __name__)

@tag.route('/tag', methods=['POST'])
def add_tag() -> Response:
    return controllers.add_tag(request)

@tag.route('/tags', methods=['GET'])
def get_tags() -> Response:
    return controllers.get_tags(request)

@tag.route('/tag/<tag_id>', methods=['GET'])
def get_tag(tag_id) -> Response:
    return controllers.get_tag(request, tag_id)

@tag.route('/tag/<tag_id>', methods=['PUT'])
def update_tag(tag_id) -> Response:
    return controllers.update_tag(request, tag_id)

@tag.route('/tag/<tag_id>', methods=['DELETE'])
def delete_tag(tag_id) -> Response:
    return controllers.delete_tag(request, tag_id)