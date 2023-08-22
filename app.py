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
from models.expense_tag_mapping import ExpenseTagMapping

from routes.user_routes import user
from routes.authentication_routes import auth

load_dotenv()

database_pre = os.environ.get("DATABASE_PRE")
database_addr = os.environ.get("DATABASE_ADDR")
database_user = os.environ.get("DATABASE_USER")
database_port = os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")

first_name = os.environ.get("first_name")
last_name = os.environ.get("last_name")
user_name = os.environ.get("user_name")
email = os.environ.get("email")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_pre}{database_addr}:{database_port}/{database_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app, db)
ma = Marshmallow(app)

app.register_blueprint(user)
app.register_blueprint(auth)

def create_all():
    with app.app_context():
        print("Creating Tables")
        db.create_all()
        
        print("Checking to see if Admin exists...")
        user = Users.query.filter_by(email=email).first()
        if not user:
            print(f"MattC not found! Creating user for Administrator")
            
            password = input(f"Enter password for {email}: ")
            
            hashed_password = bcrypt.generate_password_hash(password).decode("utf8")
            
            new_user = Users(
                first_name=first_name,
                last_name=last_name,
                user_name=user_name,
                email=email,
                password=hashed_password
            )
            
            db.session.add(new_user)
            db.session.commit()
            print("User created.")
        else:
            print(f"user with the email: {email} found.")

        print("All Done")

CORS(app)
bcrypt = Bcrypt(app)

if __name__ == '__main__':
    create_all()
    app.run(host="0.0.0.0", port=8086)
