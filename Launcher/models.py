__author__ = 'HZ'


from .import db
from flask_security import UserMixin, RoleMixin


class Machine(db.Model):
    """Server Machine model....remote host"""
    id = db.Column(db.Integer, primary_key=True)
    host_name = db.Column(db.Text)
    host_ip = db.Column(db.Text)
    host_address = db.Column(db.Text)
    ssh_username = db.Column(db.Text)
    ssh_password = db.Column(db.Text)
    ssh_port = db.Column(db.Integer)
    mysql_username = db.Column(db.Text)
    mysql_password = db.Column(db.Text)

    def save(self):
        print 'saving'
        super(Machine, self).__save__()


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
    server_id = db.Column(db.Text)#, db.ForeignKey('machine.id', ondelete='CASCADE'))
    instance_port = db.Column(db.Integer)
    project_dir = db.Column(db.Text)

    vcs_tool = db.Column(db.Text)
    vcs_repo = db.Column(db.Text)

    mysql_db_name = db.Column(db.Text)

    is_deployed = db.Column(db.Text)
    celery_task_id = db.Column(db.Text)


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

