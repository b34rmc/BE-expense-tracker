from flask import request, Response, Blueprint

import controllers

profile = Blueprint('profile', __name__)

@profile.route('/profile', methods=['PUT'])
def profile_update() -> Response:
    return controllers.profile_update(request)