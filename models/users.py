from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma

from db import db


class Users(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    user_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    profile_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Profile.profile_id"), nullable=False)
    
    authentication = db.relationship('Authentication', backref='user')
    profile = db.relationship('Profile', back_populates='users')
    
    def __init__(self, first_name, last_name, user_name, email, password, profile_id):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.email = email
        self.password = password
        self.profile_id = profile_id
        
    def get_new_user():
        return Users("", "", "", "", "", "")
    
    
class UsersSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'first_name', 'last_name', 'user_name', 'email', 'profile_id', 'profile']
    profile = ma.fields.Nested("ProfileSchema")
        

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)