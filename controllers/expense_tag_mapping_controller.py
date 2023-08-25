from flask import jsonify
import flask
from db import db
from models.expense_tag_mapping import ExpenseTagMapping, expense_tag_mapping_schema, expenses_tag_mapping_schema

from util.reflection import populate_object, is_valid_uuid
from util.authenticate import authenticate


@authenticate
def add_map(req: flask.Request, auth_info) -> flask.Response:
    post_data = req.json
    new_map = ExpenseTagMapping.get_new_expense_tag_mapping()
    
    populate_object(new_map, post_data)
    
    if not new_map.expense_id:
        return jsonify("expense_id required")
    
    if not new_map.tag_id:
        return jsonify("tag_id required")
    
    db.session.add(new_map)
    db.session.commit()
    
    return jsonify(expense_tag_mapping_schema.dump(new_map)), 201
    
@authenticate
def get_maps(req: flask.Request, auth_info) -> flask.Response:
    all_maps = db.session.query(ExpenseTagMapping).all() 
    
    if not all_maps:
        return jsonify("no maps found")
    
    serialized_maps = [mapping.serialize() for mapping in all_maps]
    return jsonify({'expense_tag_mappings': serialized_maps}), 200
    

@authenticate
def get_map(req: flask.Request, map_id, auth_info) -> flask.Response:
    if not is_valid_uuid(map_id):
        return jsonify("Invalid map_id"), 400
    
    map_record = db.session.query(ExpenseTagMapping).filter_by(map_id=map_id).first()
    
    if map_record:
        return jsonify(expense_tag_mapping_schema.dump(map_record)), 200
    
    return jsonify("map not found"), 404

@authenticate
def update_map(req: flask.Request, map_id, auth_info) -> flask.Response:
    if not is_valid_uuid(map_id):
        return jsonify("Invalid tag_id"), 400
    data = req.get_json()
    
    map = ExpenseTagMapping.query.filter_by(map_id=map_id).first()
    
    if not map:
        return jsonify("map not found"), 404
    
    populate_object(map, data)

    if not data:
        return jsonify("no fields to update"), 400
    
    db.session.commit()
    
    return jsonify({"message": " map successfully updated", " tag": expense_tag_mapping_schema.dump(map)}), 200
    
@authenticate
def delete_map(req: flask.Request, map_id, auth_info) -> flask.Response:
    if not is_valid_uuid(map_id):
        return jsonify("Invalid map_id"), 400
    map = ExpenseTagMapping.query.filter_by(map_id=map_id).first()
    
    if not map:
        return jsonify("map not found"), 404
    
    db.session.delete(map)
    db.session.commit()
    
    return jsonify("map Deleted"), 200