from flask_bcrypt import Bcrypt
from flask import jsonify
import flask
from db import db
from uuid import UUID
from models.users import Users, user_schema, users_schema
from models.expense import Expense, expense_schema, expenses_schema

from util.reflection import populate_object, is_valid_uuid
from util.authenticate import authenticate


@authenticate
def expense_add(req: flask.Request, auth_info) -> flask.Response:
    post_data = req.json
    new_expense = Expense.get_new_expense()
    
    populate_object(new_expense, post_data)
    
    new_expense.user_id = auth_info.user_id
    
    if not new_expense.category_id:
        return jsonify("category_id required"), 400
    
    if not new_expense.user_id:
        return jsonify("user_id required"), 400
    
    if not new_expense.amount:
        return jsonify("amount required"), 400
    
    db.session.add(new_expense)
    db.session.commit()
    
    return expense_schema.dump(new_expense), 201
    
@authenticate
def get_expenses(req: flask.Request, auth_info) -> flask.Response:
    all_expenses = db.session.query(Expense).all() 
    
    if all_expenses:
        return jsonify(expenses_schema.dump(all_expenses)), 200
    
    return jsonify("no expenses found"), 404

@authenticate
def get_expense(req: flask.Request, expense_id, auth_info) -> flask.Response:
    if not is_valid_uuid(expense_id):
        return jsonify("Invalid expense_id"), 400
    
    expense_record = db.session.query(Expense).filter_by(expense_id=expense_id).first()
    
    if expense_record:
        return jsonify(expense_schema.dump(expense_record)), 200
    
    return jsonify("User not found"), 404

@authenticate
def update_expense(req: flask.Request, expense_id, auth_info) -> flask.Response:
    if not is_valid_uuid(expense_id):
        return jsonify("Invalid expense_id"), 400
    
    data = req.get_json()
    
    expense = Expense.query.filter_by(expense_id=expense_id).first()
    
    if not expense:
        return jsonify("Expense not found"), 404
    
    populate_object(expense, data)
    
    if not data:
        return jsonify("no fields to update"), 400

    db.session.commit()
    
    return jsonify("successfully updated expense", expense_schema.dump(expense)), 200
    
@authenticate
def delete_expense(req: flask.Request, expense_id, auth_info) -> flask.Response:
    expense = Expense.query.filter_by(expense_id=expense_id).first()
    
    if not expense:
        return jsonify("Expense not found"), 404
    
    db.session.delete(expense)
    db.session.commit()
    
    return jsonify("Expense Deleted"), 200