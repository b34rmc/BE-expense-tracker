from flask import jsonify, Response, request
from flask_bcrypt import check_password_hash
from datetime import datetime, timedelta
from db import db
from models.users import Users
from models.authentication import Authentication, authentication_schema

def auth_token_add(req: request) -> Response:
    post_data = req.json
    
    email = post_data.get("email")
    password = post_data.get("password")
    
    user = Users.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password, password):
        expiration = datetime.utcnow() + timedelta(hours=18)
        new_auth_token = Authentication(user_id=user.user_id, expiration=expiration)
        
        db.session.add(new_auth_token)
        db.session.commit()
        
        return jsonify({"message": "Auth-Token added", "auth": authentication_schema.dump(new_auth_token)}), 201
    else:
        return jsonify({"error": "Invalid email or password"}), 401

def auth_token_remove(req: request) -> Response:
    post_data = req.get_json()
    print("post_data", post_data)
    auth_token = None
    if post_data:
        auth_token = post_data.get("auth_token")
    
    auth_record = Authentication.query.filter_by(auth_token=auth_token).first()
    
    if auth_record:
        db.session.delete(auth_record)
        db.session.commit()
        return jsonify({"message": "Authentication token removed"}), 200
    else:
        return jsonify({"error": "Authentication token not found"}), 404

def auth_token_remove_expired(req: request) -> Response:
    expired_auth_tokens = Authentication.query.filter(Authentication.expiration < datetime.utcnow()).all()
    
    for auth_token in expired_auth_tokens:
        db.session.delete(auth_token)
    
    db.session.commit()
    
    return jsonify({"message": f"Removed {len(expired_auth_tokens)} expired authentication tokens"}), 200