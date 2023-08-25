from flask import jsonify
import flask
from db import db
from models.expense_tag import ExpenseTag, expense_tag_schema, expenses_tag_schema

from util.reflection import populate_object, is_valid_uuid
from util.authenticate import authenticate


@authenticate
def add_tag(req: flask.Request, auth_info) -> flask.Response:
    post_data = req.json
    new_tag = ExpenseTag.get_new_tag()
    
    populate_object(new_tag, post_data)
    
    if not new_tag.tag_name:
        return jsonify("tag_name required")
    
    db.session.add(new_tag)
    db.session.commit()
    
    return expense_tag_schema.dump(new_tag), 201
    
@authenticate
def get_tags(req: flask.Request, auth_info) -> flask.Response:
    all__tags = db.session.query(ExpenseTag).all() 
    
    if not all__tags:
        return jsonify("no tags found")
    
    return jsonify(expenses_tag_schema.dump(all__tags)), 200
    

@authenticate
def get_tag(req: flask.Request, tag_id, auth_info) -> flask.Response:
    if not is_valid_uuid(tag_id):
        return jsonify("Invalid tag_id"), 400
    
    tag_record = db.session.query(ExpenseTag).filter_by(tag_id=tag_id).first()
    
    if tag_record:
        return jsonify(expense_tag_schema.dump(tag_record)), 200
    
    return jsonify("tag not found"), 404

@authenticate
def update_tag(req: flask.Request, tag_id, auth_info) -> flask.Response:
    if not is_valid_uuid(tag_id):
        return jsonify("Invalid tag_id"), 400
    data = req.get_json()
    
    tag = ExpenseTag.query.filter_by(tag_id=tag_id).first()
    
    if not tag:
        return jsonify("tag not found"), 404
    
    populate_object(tag, data)

    if not data:
        return jsonify("no fields to update"), 400
    
    db.session.commit()
    
    return jsonify({"message": " tag successfully updated", " tag": expense_tag_schema.dump(tag)}), 200
    
@authenticate
def delete_tag(req: flask.Request, tag_id, auth_info) -> flask.Response:
    if not is_valid_uuid(tag_id):
        return jsonify("Invalid tag_id"), 400
    tag = ExpenseTag.query.filter_by(tag_id=tag_id).first()
    
    if not tag:
        return jsonify("tag not found"), 404
    
    db.session.delete(tag)
    db.session.commit()
    
    return jsonify("tag Deleted"), 200