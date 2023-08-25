from functools import wraps
from flask import request, jsonify
from datetime import datetime
from models.authentication import Authentication  # Import the Authentication model

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_token = request.headers.get("Auth-Token")
        if not auth_token:
            return jsonify({"error": "auth_token missing"}), 401
        
        auth_record = Authentication.query.filter_by(auth_token=auth_token).first()
        
        if not auth_record:
            return jsonify({"error": "Invalid auth_token"}), 401
        
        current_time = datetime.utcnow()
        if auth_record.expiration and auth_record.expiration < current_time:
            return jsonify({"error": "Expired auth_token"}), 401
        
        return func(auth_info=auth_record, *args, **kwargs)
    
    return wrapper

