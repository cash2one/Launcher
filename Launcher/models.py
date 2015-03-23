# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from flask_user import UserMixin
from .import db

# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # User email information (required for Flask-User)
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String(50), nullable=False, server_default='')
    last_name = db.Column(db.String(50), nullable=False, server_default='')

    # Other credentials
    svn_username = db.Column(db.Text)
    svn_password = db.Column(db.Text)
    git_username = db.Column(db.Text)
    git_password = db.Column(db.Text)


    # Relationships
    user_auth = db.relationship('UserAuth', uselist=False)
    roles = db.relationship('Role', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'))


# Define the UserAuth data model.
class UserAuth(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))

    # User authentication information (required for Flask-User)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # Relationships
    user = db.relationship('User', uselist=False)


# Define the Role data model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))


# Define the UserRoles association model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


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


class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    client_name = db.Column(db.Text)
    product_type = db.Column(db.Text)
    server_id = db.Column(db.Integer(), db.ForeignKey('machine.id', ondelete='CASCADE'))
    instance_port = db.Column(db.Integer)
    project_dir = db.Column(db.Text)

    vcs_tool = db.Column(db.Text)
    vcs_repo = db.Column(db.Text)

    mysql_db_name = db.Column(db.Text)
