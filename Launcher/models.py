"""
Module: models.py
Author: HZ
Created: March 25, 2015

Description: 'Models for the project'
"""


from .import db
from flask_security import UserMixin, RoleMixin
from sqlalchemy import event
from utils import pwd_encryption, pwd_decryption


class Task(db.Model):
    """Single Task model....to execute seperate command"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    cmd = db.Column(db.Text)
    params = db.Column(db.Text)
    switches = db.Column(db.Text)
    arguments = db.Column(db.Text)
    stage = db.Column(db.Text)


class Product(db.Model):
    """Products model....software products of office"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    language = db.Column(db.Text)
    framework = db.Column(db.Text)
    deploy_steps = db.Column(db.Text)
    maintain_steps = db.Column(db.Text)
    vcs_repo_base = db.Column(db.Text)


class Project(db.Model):
    """Project model.....to deploy a new project on a remote host"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    client_name = db.Column(db.Text)
    product_type = db.Column(db.Text)
    #server_id = db.Column(db.Text)#, db.ForeignKey('machine.id', ondelete='CASCADE'))
    server_id = db.Column(db.Integer, db.ForeignKey('machine.id'))
    instance_port = db.Column(db.Integer)
    project_dir = db.Column(db.Text)

    vcs_tool = db.Column(db.Text)
    vcs_repo = db.Column(db.Text)

    rdbms = db.Column(db.Text)
    db_name = db.Column(db.Text)

    is_deployed = db.Column(db.Text)
    celery_task_id = db.Column(db.Text)


class Machine(db.Model):
    """Server Machine model....remote host"""
    id = db.Column(db.Integer, primary_key=True)
    host_name = db.Column(db.Text)
    host_ip = db.Column(db.Text)
    host_address = db.Column(db.Text)
    ssh_username = db.Column(db.Text)
    ssh_password = db.Column(db.Text)
    ssh_port = db.Column(db.Integer)
    #ToDO: Various db system?.....should another table be created?!
    db_username = db.Column(db.Text)
    db_password = db.Column(db.Text)

    projects = db.relationship('Project', backref='machine')


@event.listens_for(Machine, 'before_insert')
def receive_before_insert(mapper, connection, target):
    """listen for the 'before_insert' event"""
    target.ssh_password = pwd_encryption(target.ssh_password)
    target.db_password = pwd_encryption(target.db_password)

@event.listens_for(Machine, 'before_update')
def receive_before_update(mapper, connection, target):
    """listen for the 'before_update' event"""
    from sqlalchemy.orm.attributes import get_history

    ssh_pass_hist = get_history(target, 'ssh_password')
    added, unchanged, deleted = ssh_pass_hist

    try:
        if added[0] == pwd_decryption(deleted[0]):
            #print 'same'
            target.ssh_password = deleted[0]
        else:
            #print 'not same'
            target.ssh_password = pwd_encryption(target.ssh_password)
    except Exception as e:
        print e
        target.ssh_password = pwd_encryption(target.ssh_password)

    db_pass_hist = get_history(target, 'db_password')
    added, unchanged, deleted = db_pass_hist

    try:
        if added[0] == pwd_decryption(deleted[0]):
            #print 'same'
            target.db_password = deleted[0]
        else:
            #print 'not same'
            target.db_password = pwd_encryption(target.db_password)
    except Exception as e:
        print e
        target.db_password = pwd_encryption(target.db_password)


class Message(db.Model):
    """Message model....intercom test"""
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Text)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver = db.Column(db.Text)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject_topic = db.Column(db.Text)
    message_body = db.Column(db.Text)
    sent_at = db.Column(db.Text)
    read = db.Column(db.Boolean)


#Flask-Security models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    """User role model"""
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    #Tracking
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer())
    #Personal Info: More to add later
    display_name = db.Column(db.String(255), unique=True)
    full_name = db.Column(db.String(255))
    svn_username = db.Column(db.String(255))
    svn_password = db.Column(db.String(255))


    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    msgs_sent = db.relationship('Message', backref=db.backref('owner', lazy='dynamic'), primaryjoin="User.id==Message.sender_id")
    msgs_received = db.relationship('Message', backref=db.backref('receipient', lazy='dynamic'), primaryjoin="User.id==Message.receiver_id")
    msgs_unread = db.relationship('Message', primaryjoin="and_(User.id==Message.receiver_id, Message.read==0)")


# @event.listens_for(User, 'before_insert')
# def receive_before_insert(mapper, connection, target):
#     """listen for the 'before_insert' event"""
#     target.svn_password = pwd_encryption(target.svn_password)

@event.listens_for(User, 'before_update')
def receive_before_update(mapper, connection, target):
    """listen for the 'before_update' event"""
    from sqlalchemy.orm.attributes import get_history
    hist = get_history(target, 'svn_password')
    added, unchanged, deleted = hist

    try:
        if added[0] == pwd_decryption(deleted[0]):
            #print 'same'
            target.svn_password = deleted[0]
        else:
            #print 'not same'
            target.svn_password = pwd_encryption(target.svn_password)
    except Exception as e:
        print e
        target.svn_password = pwd_encryption(target.svn_password)


