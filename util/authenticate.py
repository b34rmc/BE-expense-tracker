from functools import wraps
from flask import request, jsonify
from datetime import datetime
from db import db
from models.authentication import Authentication


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_token = request.headers.get("Auth-Token")
        if not auth_token:
            return jsonify({"error": "auth_token missing"}), 401
        
        auth_record = Authentication.query.filter_by(auth_token=auth_token).first()
        
        if not auth_record or auth_record.expiration < datetime.utcnow():
            return jsonify({"error": "Invalid or expired auth_token"}), 401
        
        return func(auth_info=auth_record, *args, **kwargs)
    
    return wrapper
