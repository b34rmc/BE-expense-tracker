import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from db import db


class ExpenseTag(db.Model):
    __tablename__ = 'ExpenseTag'
    tag_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    tag_name  = db.Column(db.String(), nullable=False)
    background_color = db.Column(db.String(), default='#18181B', nullable=False)
    
    
    def __init__(self, tag_name, background_color='#18181B'):
        self.tag_name = tag_name
        self.background_color = background_color
        
    def get_new_tag():
        return ExpenseTag("")
        
        
class ExpenseTagSchema(ma.Schema):
    class Meta:
        fields = ['tag_id', 'tag_name', 'background_color']
        
        
expense_tag_schema = ExpenseTagSchema()
expenses_tag_schema = ExpenseTagSchema(many=True)