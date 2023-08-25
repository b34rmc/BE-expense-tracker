from flask import request, Response, Blueprint

import controllers

mapping = Blueprint('mapping', __name__)

@mapping.route('/map', methods=['POST'])
def add_map() -> Response:
    return controllers.add_map(request)

@mapping.route('/maps', methods=['GET'])
def get_maps() -> Response:
    return controllers.get_maps(request)

@mapping.route('/map/<map_id>', methods=['GET'])
def get_map(map_id) -> Response:
    return controllers.get_map(request, map_id)

@mapping.route('/map/<map_id>', methods=['PUT'])
def update_map(map_id) -> Response:
    return controllers.update_map(request, map_id)

@mapping.route('/map/<map_id>', methods=['DELETE'])
def delete_map(map_id) -> Response:
    return controllers.delete_map(request, map_id)