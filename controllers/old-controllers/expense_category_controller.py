from flask import jsonify
import flask
from db import db
from models.expense_category import ExpenseCategory, expense_category_schema, expenses_category_schema

from util.reflection import populate_object, is_valid_uuid
from util.authenticate import authenticate


@authenticate
def add_category(req: flask.Request, auth_info) -> flask.Response:
    post_data = req.json
    new_expense_category = ExpenseCategory.get_new_expense_category()
    
    populate_object(new_expense_category, post_data)
    
    if not new_expense_category.category_name:
        return jsonify("category_name required")
    
    db.session.add(new_expense_category)
    db.session.commit()
    
    return expense_category_schema.dump(new_expense_category), 201
    
@authenticate
def get_categories(req: flask.Request, auth_info) -> flask.Response:
    all_expense_categories = db.session.query(ExpenseCategory).all() 
    
    if not all_expense_categories:
        return jsonify("no categories found")
    
    return jsonify(expenses_category_schema.dump(all_expense_categories)), 200
    

@authenticate
def get_category(req: flask.Request, category_id, auth_info) -> flask.Response:
    if not is_valid_uuid(category_id):
        return jsonify("Invalid uuid"), 400
    
    category_record = db.session.query(ExpenseCategory).filter_by(category_id=category_id).first()
    
    if category_record:
        return jsonify(expense_category_schema.dump(category_record)), 200
    
    return jsonify("Category not found"), 404

@authenticate
def update_category(req: flask.Request, category_id, auth_info) -> flask.Response:
    data = req.get_json()
    if not is_valid_uuid(category_id):
        return jsonify("Invalid category_id"), 404
    
    category = ExpenseCategory.query.filter_by(category_id=category_id).first()
    
    if not category:
        return jsonify("category not found"), 404
    
    populate_object(category, data)

    db.session.commit()
    
    return jsonify({"message": "expense category successfully updated", "expense category": expense_category_schema.dump(category)}), 200
    
@authenticate
def delete_category(req: flask.Request, category_id, auth_info) -> flask.Response:
    category = ExpenseCategory.query.filter_by(category_id=category_id).first()
    
    if not category:
        return jsonify("category not found"), 404
    
    db.session.delete(category)
    db.session.commit()
    
    return jsonify("Category Deleted"), 200