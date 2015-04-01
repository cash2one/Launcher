__author__ = 'HZ'
#package

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask.ext.security import Security, SQLAlchemyUserDatastore
from celery import Celery

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Initialize Flask-Mail
mail = Mail(app)

# Setup Flask-Security
from models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Initialize Celery
celery_obj = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery_obj.conf.update(app.config)

from .import views, models