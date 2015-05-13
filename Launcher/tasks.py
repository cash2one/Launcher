__author__ = 'HZ'

from .import celery_obj, app, mail, security


# Async Email sending
# Setup the task
@celery_obj.task
def send_security_email(msg):
    # Use the Flask-Mail extension instance to send the incoming ``msg`` parameter
    # which is an instance of `flask_mail.Message`
    with app.app_context():
        mail.send(msg)


@security.send_mail_task
def delay_security_email(msg):
    send_security_email.delay(msg)