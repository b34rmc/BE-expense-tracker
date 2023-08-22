import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from db import db


class ExpenseTagMapping(db.Model):
    __tablename__ = 'ExpenseTagMapping'
    mapping_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    expense_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Expense.expense_id'), nullable=False)
    tag_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ExpenseTag.tag_id'), nullable=False)
    
    
    def __init__(self, expense_id, tag_id):
        self.expense_id = expense_id
        self.tag_id = tag_id
        
        
class ExpenseTagMappingSchema(ma.Schema):
    class Meta:
        fields = ['mapping_id', 'expense_id', 'tag_id']
        
        
expense_tag_mapping_schema = ExpenseTagMappingSchema()
expenses_tag_mapping_schema = ExpenseTagMappingSchema(many=True)