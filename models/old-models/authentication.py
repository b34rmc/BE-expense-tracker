import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db
from models.users import UsersSchema

class Authentication(db.Model):
    __tablename__ = 'Authentication'
    auth_token = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)
    expiration = db.Column(db.DateTime(), nullable=False)
    
    def __init__(self, user_id, expiration):
        self.user_id = user_id
        self.expiration = expiration
        
        
class AuthenticationSchema(ma.Schema):
    class Meta:
        fields = ['auth_token', 'user', 'expiration']
        
    user = ma.fields.Nested(UsersSchema(only=['first_name', 'last_name', 'email', 'user_name', 'user_id']))
    

authentication_schema = AuthenticationSchema()