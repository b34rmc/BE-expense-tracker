from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask
from flask_bcrypt import Bcrypt

from db import db, init_db
import os
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv

from models.users import Users
from models.authentication import Authentication
from models.expense import Expense
from models.expense_category import ExpenseCategory
from models.expense_tag import ExpenseTag
from models.profile_image import Profile

from routes.user_routes import user
from routes.profile_routes import profile
from routes.expense_routes import expense
from routes.expense_category_routes import category
from routes.expense_tag_routes import tag
from routes.expense_tag_mapping_routes import mapping
from routes.authentication_routes import auth

import config

load_dotenv()

database_pre = os.environ.get("DATABASE_PRE")
database_addr = os.environ.get("DATABASE_ADDR")
database_user = os.environ.get("DATABASE_USER")
database_port = os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_pre}{database_addr}:{database_port}/{database_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app, db)
ma = Marshmallow(app)

app.register_blueprint(user)
app.register_blueprint(profile)
app.register_blueprint(expense)
app.register_blueprint(category)
app.register_blueprint(tag)
app.register_blueprint(mapping)
app.register_blueprint(auth)

def create_all():
    with app.app_context():
        print("Creating Tables")
        db.create_all()
        
        print("Checking to see if Admin exists...")
        user = Users.query.filter_by(user_id=config.user_id).first()
        if not user:
            print("Admin not found! Creating user for Admin...")
            print("Creating Profile...")
            new_profile = Profile(
                position_x=config.position_x,
                position_y=config.position_y,
                image_url=config.image_url
            )
            db.session.add(new_profile)
            db.session.commit()
            print("profile created")
            
            print("creating expense category...")
            new_expense_category = ExpenseCategory(
                category_name=config.category_name,
                description=config.description
            )
            db.session.add(new_expense_category)
            db.session.commit()
            print("expense category created")
            
            password = input(f"\n\nCreate password for {config.email}: ")
            hashed_password = bcrypt.generate_password_hash(password).decode("utf8")
            profile_id = new_profile.profile_id
            
            new_user = Users(
                first_name=config.first_name,
                last_name=config.last_name,
                user_name=config.user_name,
                email=config.email,
                password=hashed_password,
                profile_id=profile_id
            )
            
            try:
                db.session.add(new_user)
                db.session.commit()
                print("User created.")
            except Exception as e:
                print(f"Error creating user: {e}")
                db.session.rollback()
        else:
            print(f"user with the email: {user.email} found.")

        print("All Done")

CORS(app)
bcrypt = Bcrypt(app)

if __name__ == '__main__':
    create_all()
    app.run(host="0.0.0.0", port=8089, debug=True)