__author__ = 'HZ'
#package

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_user import SQLAlchemyAdapter, UserManager

from celery import Celery

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Initialize Flask-Mail
mail = Mail(app)

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from models import User, UserAuth

# Setup Flask-User
db_adapter = SQLAlchemyAdapter(db, User, UserAuthClass=UserAuth)  # Register the User model
user_manager = UserManager(db_adapter, app)  # Initialize Flask-User

from .import views, models