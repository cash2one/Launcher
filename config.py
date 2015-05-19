#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module: config.py
Author: HZ
Created: Mar 23, 2015

Description: 'The Flask Configuration File. Also contains other required configurations.'
"""

# global imports below: built-in, 3rd party, own
import os
basedir = os.path.abspath(os.path.dirname(__file__))


# Ownership information
__author__ = 'HZ'
__copyright__ = "Copyright 2015, HZ, Divine IT Ltd."
__credits__ = ["HZ"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "HZ"
__email__ = "hz.ce06@gmail.com"
__status__ = "Development"


# Flask-SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'launcher.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
#SQLALCHEMY_ECHO = True
#SQLALCHEMY_RECORD_QUERIES = True

# Flask-WTF settings
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# Flask-Babel
BABEL_DEFAULT_TIMEZONE = 'Asia/Dhaka'

# Flask-Mail settings
MAIL_USERNAME = 'palash@divine-it.net'
MAIL_PASSWORD = 'hpkjhulvnhekbdmz'
#MAIL_PASSWORD = '1234'
#MAIL_DEFAULT_SENDER = ''
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False

# Celery configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
#CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
#TIME_ZONE = 'UTC'
#USE_TZ = True
#CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Asia/Dhaka'
CELERY_RESULT_BACKEND = 'db+sqlite:///launcher.db'
#CELERY_TASK_RESULT_EXPIRES = 18000  # 5 hours.
#CELERY_SEND_TASK_SENT_EVENT = True
# Enables error emails.
CELERY_SEND_TASK_ERROR_EMAILS = True
# Name and email addresses of recipients
ADMINS = (
    ('HZ', 'palash@divine-it.net'),
)
# Mailserver configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'palash@divine-it.net'
EMAIL_HOST_PASSWORD = 'hpkjhulvnhekbdmz'
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
# Email address used as sender (From field).
SERVER_EMAIL = 'no-reply@launcher.celery.com'

# Flask-Security Settings

#SITE_NAME = 'Flask Site'
#LOG_LEVEL = logging.DEBUG

#MEMCACHED_SERVERS = ['localhost:11211']
#SYS_ADMINS = ['foo@example.com']

# Flask-Security setup
SECURITY_EMAIL_SENDER = 'HZ < Admin >'
SECURITY_LOGIN_WITHOUT_CONFIRMATION = False
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True
SECURITY_CONFIRMABLE = True
SECURITY_TRACKABLE = True
SECURITY_URL_PREFIX = '/auth'
SECUIRTY_POST_LOGIN = '/'
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
# import uuid; salt = uuid.uuid4().hex
SECURITY_PASSWORD_SALT = '2b8b74efc58e489e879810905b6b6d4dc6'
SECURITY_UNAUTHORIZED_VIEW = '/page_not_serveable'

# CACHE
#CACHE_TYPE = 'simple'

# Debug mode
DEBUG = True