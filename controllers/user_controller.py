from flask_bcrypt import Bcrypt
from flask import jsonify
import flask
from db import db
from uuid import UUID
from models.users import Users, user_schema, users_schema

from util.reflection import populate_object, is_valid_uuid
from util.authenticate import authenticate

bcrypt = Bcrypt()

@authenticate
def add_user(req: flask.Request, auth_info) -> flask.Response:
    post_data = req.get_json()
    new_user = Users.get_new_user()
    
    populate_object(new_user, post_data)
    
    if not new_user.password:
        return jsonify({"message": "password is required"}), 400
    
    new_user.password = bcrypt.generate_password_hash(new_user.password).decode("utf8")
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(user_schema.dump(new_user), 201)
    

def get_users(req: flask.Request) -> flask.Response:
    all_users = db.session.query(Users).all() 
    
    if all_users:
        return jsonify(users_schema.dump(all_users)), 200
    
    return jsonify("no users found"), 404


def get_user(req: flask.Request, user_id) -> flask.Response:
    if not is_valid_uuid(user_id):
        return jsonify("Invalid user_id"), 400
    
    user_record = db.session.query(Users).filter_by(user_id=user_id).first()
    
    if user_record:
        return jsonify(user_schema.dump(user_record)), 200
    
    return jsonify("User not found"), 404


def update_user(req: flask.Request, user_id) -> flask.Response:
    if not is_valid_uuid(user_id):
        return jsonify("Invalid user id"), 404
    
    data = req.get_json()
    
    user = Users.query.filter_by(user_id=user_id).first()
    
    if not user:
        return jsonify("User not found"), 404
    
    populate_object(user, data)

    db.session.commit()
    
    return jsonify(user_schema.dump(user)), 200
    

def delete_user(req: flask.Request, user_id) -> flask.Response:
    user = Users.query.filter_by(user_id=user_id).first()
    
    if not user:
        return jsonify("User not found"), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify("User Deleted"), 200