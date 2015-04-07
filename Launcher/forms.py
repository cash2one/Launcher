__author__ = 'HZ'


from flask_wtf import Form
from wtforms import StringField, SubmitField, validators, SelectField, IntegerField, widgets, SelectMultipleField, PasswordField


class MultiCheckboxField(SelectMultipleField):
    """Required for rendering checkbox!"""
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class CmdExecuteForm(Form):
    cmd = StringField(validators=[validators.DataRequired()])


class TaskExecuteForm(Form):
    cmd = StringField(validators=[validators.DataRequired()])
    params = StringField()
    switches = StringField()
    arguments = StringField()


# Project Add Form
class ProjectAddEditForm(Form):
    """Form for adding new project"""
    name = StringField(label='Project Name', validators=[validators.DataRequired("Must give a project name")])
    client_name = StringField(label='Client Name')
    product_type = SelectField(label='Product Type', validators=[validators.DataRequired()])
    server = SelectField(label='Server Machine', validators=[validators.DataRequired()])
    instance_port = IntegerField(label='Instance Port #', validators=[validators.DataRequired("Must provide an integer port")])
    project_dir = StringField(label='Project Directory', validators=[validators.DataRequired("Must be valid path")])
    vcs_tool = SelectField(label='Version Control Tool', choices=[('SVN', 'SubVersioN'),('Git', 'Git')])
    vcs_repo = StringField(label='VCS Repository URL', validators=[validators.DataRequired()])
    mysql_database_name = StringField(label='Database Name', validators=[validators.DataRequired()])


class ProductAddEditForm(Form):
    """Form for adding new product"""
    name = StringField(label='Product Name', validators=[validators.DataRequired('Must give the product name')])
    language = SelectField(label='Coding Language', choices=[('Python', 'Python'), ('PHP', 'PHP'), ('Perl', 'Perl'),('Java', 'Java'),('Ruby', 'Ruby')])
    framework = SelectField(label='Framework', choices=[('FurinaPy', 'FurinaPy'), ('FurinaPHP', 'FurinaPHP'), ('django', 'django'), ('Flask', 'Flask'), ('Cake', 'Cake')])
    deploy_steps = StringField(label='Steps needed to deploy this type of product:')
    maintain_steps = StringField(label='Steps needed to maintain this type of product:')
    vcs_repo_base = StringField(label='Version Control Repository Base URL')


class TaskAddEditForm(Form):
    """Form for adding new task"""
    name = StringField(label='Task Name', validators=[validators.DataRequired()])
    description = StringField(label='Description')
    cmd = StringField(label='Command', validators=[validators.DataRequired()])
    params = StringField(label='Parameters')
    switches = StringField(label='Switches')
    arguments = StringField(label='Arguments')
    stage = SelectField(label='Stage', choices=[('general', 'General'), ('deployment', 'Deployment'), ('maintenance', 'Maintenance')])


class UserRoleForm(Form):
    """Form for assigning roles to an User"""
    user = SelectField(label='Select an User:', coerce=str)
    roles = MultiCheckboxField(label='Roles', coerce=str)


class RoleCreateForm(Form):
    """Form for creating new roles for users"""
    name = StringField(label='Name of the role:', validators=[validators.DataRequired('Must give a role name')])
    description = StringField(label='Enter a description of the role:', validators=[validators.DataRequired('Must describe the role (eg Administrator, Moderator)...This will be shown when assigning role')])


class ServerMachineAddEditForm(Form):
    """Form for adding new server"""
    host_name = StringField(label='Host Name')
    host_ip = StringField(label='Host IP Address', validators=[validators.IPAddress(), validators.DataRequired()])
    host_address = StringField(label='Host Address', validators=[validators.DataRequired()])
    ssh_username = StringField(label='SSH Username', validators=[validators.DataRequired()])
    ssh_password = PasswordField(label='SSH Password', validators=[validators.DataRequired()])
    ssh_port = IntegerField(label='SSH Port', validators=[validators.DataRequired()])
    mysql_username = StringField(label='MySQL Username', validators=[validators.DataRequired()])
    mysql_password = PasswordField(label='MySQL Password', validators=[validators.DataRequired()])


class ProfileEditForm(Form):
    """Form for modifying profile info"""
    display_name = StringField(label='Display Name to be shown after login:')
    full_name = StringField(label='Your Full Name:')
    svn_username = StringField(label='Your SVN Username: (Do not enter credentials unless needed)')
    svn_password = PasswordField(label='Your SVN Password: (Do not enter credentials unless needed)')