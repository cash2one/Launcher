__author__ = 'HZ'


from .import db
from flask_security import UserMixin, RoleMixin


class Machine(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    host_name = db.Column(db.Text)
    host_ip = db.Column(db.Text)
    host_address = db.Column(db.Text)
    ssh_username = db.Column(db.Text)
    ssh_password = db.Column(db.Text)
    ssh_port = db.Column(db.Integer)
    mysql_username = db.Column(db.Text)
    mysql_password = db.Column(db.Text)


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    cmd = db.Column(db.Text)
    params = db.Column(db.Text)
    switches = db.Column(db.Text)
    arguments = db.Column(db.Text)
    stage = db.Column(db.Text)


class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    language = db.Column(db.Text)
    framework = db.Column(db.Text)
    deploy_steps = db.Column(db.Text)
    maintain_steps = db.Column(db.Text)
    vcs_repo_base = db.Column(db.Text)


class Project(db.Model):

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
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))