import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from db import db


class Expense(db.Model):
    __tablename__ = 'Expense'
    expense_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)
    category = db.Column(UUID(as_uuid=True), db.ForeignKey('ExpenseCategory.category_id'), nullable=False)
    amount = db.Column(db.String(), nullable=False)
    date = db.Column(db.Date(), default=datetime.utcnow(), nullable=False)
    description = db.Column(db.String())
    
    
    def __init__(self, user_id, category, amount, date, description):
        self.user_id = user_id
        self.category = category
        self.amount = amount
        self.date = date
        self.description = description
        
        
class ExpenseSchema(ma.Schema):
    class Meta:
        fields = ['expense_id', 'user_id', 'category', 'amount', 'date', 'description']
        
        
expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)
    