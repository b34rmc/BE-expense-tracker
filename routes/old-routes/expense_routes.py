from flask import request, Response, Blueprint

import controllers

expense = Blueprint('expense', __name__)

@expense.route('/expense', methods=['POST'])
def expense_add() -> Response:
    return controllers.expense_add(request)

@expense.route('/expenses', methods=['GET'])
def get_expenses() -> Response:
    return controllers.get_expenses(request)

@expense.route('/expense/<expense_id>', methods=['GET'])
def get_expense(expense_id) -> Response:
    return controllers.get_expense(request, expense_id)

@expense.route('/expense/<expense_id>', methods=['PUT'])
def update_expense(expense_id) -> Response:
    return controllers.update_expense(request, expense_id)

@expense.route('/expense/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id) -> Response:
    return controllers.delete_expense(request, expense_id)

