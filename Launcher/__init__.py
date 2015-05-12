__author__ = 'HZ'
#package

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask.ext.security import Security, SQLAlchemyUserDatastore
from celery import Celery
from flask.ext.babel import Babel


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Initialize Flask-Mail
mail = Mail(app)

#Initialize Flask-Babel
babel = Babel(app)

# Setup Flask-Security
from models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Initialize Celery
celery_obj = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery_obj.conf.update(app.config)

from .import views, models

# change DEBUG in config
if not app.debug:
    import logging, os
    from logging.handlers import RotatingFileHandler

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")

    # Flask-Wergzeug requests logging
    wz_logger = logging.getLogger('werkzeug')
    wz_handler = RotatingFileHandler(os.path.join('logs', 'launcher.log'))
    wz_handler.setFormatter(formatter)
    wz_handler.setLevel(logging.INFO)
    wz_logger.addHandler(wz_handler)
    # Add the handler to Flask's logger for cases where Werkzeug isn't used as the underlying WSGI server.
    app.logger.addHandler(wz_handler)

    # SQLAlchemy query logging
    sa_logger = logging.getLogger('sqlalchemy')
    sa_handler = RotatingFileHandler(os.path.join('logs', 'sql.log'))
    sa_handler.setFormatter(formatter) #may not work as expected
    sa_handler.setLevel(logging.DEBUG)
    sa_logger.addHandler(sa_handler)
    #app.logger.addHandler(sa_handler)