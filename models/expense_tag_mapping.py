import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db

class ExpenseTagMapping(db.Model):
    __tablename__ = 'ExpenseTagMapping'
    map_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    expense_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Expense.expense_id'))
    tag_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ExpenseTag.tag_id'))
    
    expense = db.relationship('Expense')
    tag = db.relationship('ExpenseTag')
    
    def __init__(self, expense_id, tag_id):
        self.expense_id = expense_id
        self.tag_id = tag_id
        
    def serialize(self):
        return {
            'map_id': str(self.map_id),
            'expense_id': str(self.expense_id),
            'tag_id': str(self.tag_id)
        }
        
    def get_new_expense_tag_mapping():
        return ExpenseTagMapping("", "")
        
        
class ExpenseTagMappingSchema(ma.Schema):
    class Meta:
        fields = ['map_id', 'expense_id', 'expense', 'tag_id', 'tag']
    expense = ma.fields.Nested("Expense")
    tag = ma.fields.Nested("ExpenseTag")
        
        
expense_tag_mapping_schema = ExpenseTagMappingSchema()
expenses_tag_mapping_schema = ExpenseTagMappingSchema(many=True)