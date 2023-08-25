import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Profile(db.Model):
    __tablename__ = 'Profile'
    profile_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    position_x = db.Column(db.String(), nullable=False)
    position_y = db.Column(db.String(), nullable=False)
    image_url = db.Column(db.String(), nullable=False)
    
    users = db.relationship("Users", back_populates="profile")
    
    def __init__(self, position_x, position_y, image_url):
        self.position_x = position_x
        self.position_y = position_y
        self.image_url = image_url
        
    def get_new_profile():
        return Profile("", "", "")
    
    
class ProfileSchema(ma.Schema):
    class Meta:
        fields = ['profile_id', 'position_x', 'position_y', 'image_url']
        

profile_schema = ProfileSchema()