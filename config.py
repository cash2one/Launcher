__author__ = 'HZ'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

#Flask-SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'launcher.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


#Flask-WTF settings
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

#Flask-Babel
BABEL_DEFAULT_TIMEZONE = 'UTC+6:00'

#Flask-Mail settings
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
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

#Flask-Security Settings

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

#Debug mode
DEBUG = True