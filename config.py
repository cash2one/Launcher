__author__ = 'HZ'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

#Flask-SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'launcher.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


#Flask-WTF settings
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'


#Flask-Mail settings
MAIL_USERNAME = 'email@example.com'
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = ''
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False


# Celery configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

