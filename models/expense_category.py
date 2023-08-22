import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from db import db


class ExpenseCategory(db.Model):
    __tablename__ = 'ExpenseCategory'
    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    category_name  = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    
    
    def __init__(self, category_name, description):
        self.category_name = category_name
        self.description = description
        
        
class ExpenseCategorySchema(ma.Schema):
    class Meta:
        fields = ['category_id', 'category_name', 'description']
        
        
expense_category_schema = ExpenseCategorySchema()
expenses_category_schema = ExpenseCategorySchema(many=True)