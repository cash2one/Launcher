#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module: Launcher
Author: HZ
Created: Mar 23, 2015

Description: 'The Launcher Application by Flask. Instantiates here. Contains imports and loggers. Depends on the modules: models, views, form, ajax, tasks, error_views etc.'
"""

# Ownership information
__author__ = 'HZ'
__copyright__ = "Copyright 2015, HZ, Divine IT Ltd."
__credits__ = ["HZ"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "HZ"
__email__ = "hz.ce06@gmail.com"
__status__ = "Development"

# global imports below: built-in, 3rd party, own
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask.ext.security import Security, SQLAlchemyUserDatastore
from celery import Celery
from flask.ext.babel import Babel
from flask.ext.socketio import SocketIO


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
from .import error_views, tasks, ajax

# SocketIO chat support initialization
socketio = SocketIO()
from chat import chat as main_blueprint
app.register_blueprint(main_blueprint)
socketio.init_app(app)


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