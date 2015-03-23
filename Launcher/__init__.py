__author__ = 'HZ'
#package

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_user import SQLAlchemyAdapter, UserManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)


from models import User, UserAuth

# Setup Flask-User
db_adapter = SQLAlchemyAdapter(db, User, UserAuthClass=UserAuth)  # Register the User model
user_manager = UserManager(db_adapter, app)  # Initialize Flask-User

from .import views, models