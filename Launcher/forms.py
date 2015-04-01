__author__ = 'HZ'


from flask_wtf import Form
from wtforms import StringField, SubmitField, validators, SelectField, IntegerField, widgets, SelectMultipleField, PasswordField


class MultiCheckboxField(SelectMultipleField):
    """Required for rendering checkbox!"""
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class CmdExecuteForm(Form):
    cmd = StringField(validators=[validators.data_required])


class TaskExecuteForm(Form):
    cmd = StringField(validators=[validators.data_required])
    params = StringField()
    switches = StringField()
    arguments = StringField()


# Project Add Form
class ProjectAddForm(Form):
    """Form for adding new project"""
    name = StringField(label='Project Name', validators=[validators.data_required])
    client_name = StringField(label='Client Name')
    product_type = SelectField(label='Product Type', validators=[validators.data_required])
    server = SelectField(label='Server Machine', validators=[validators.data_required])
    instance_port = IntegerField(label='Instance Port #', validators=[validators.data_required])
    project_dir = StringField(label='Project Directory', validators=[validators.data_required])
    vcs_tool = SelectField(label='Version Control Tool', choices=[('svn', 'SubVersioN'),('git', 'Git')])
    vcs_repo = StringField(label='VCS Repository URL', validators=[validators.data_required])
    mysql_database_name = StringField(label='Database Name', validators=[validators.data_required])


class ProductAddForm(Form):
    """Form for adding new product"""
    name = StringField(label='Product Name', validators=[validators.data_required])
    language = SelectField(label='Coding Language', choices=[('python', 'Python'), ('php', 'PHP'), ('perl', 'Perl'),('java', 'Java'),('ruby', 'Ruby')])
    framework = SelectField(label='Framework', choices=[('furinapy', 'FurinaPy'), ('furinaphp', 'FurinaPHP'), ('django', 'django'), ('flask', 'Flask'), ('cake', 'Cake')])
    vcs_repo_base = StringField(label='Version Control Repository Base URL')


class TaskAddForm(Form):
    """Form for adding new task"""
    name = StringField(label='Task Name', validators=[validators.data_required])
    description = StringField(label='Description')
    cmd = StringField(label='Command', validators=[validators.data_required])
    params = StringField(label='Parameters')
    switches = StringField(label='Switches')
    arguments = StringField(label='Arguments')
    stage = SelectField(label='Stage', choices=[('general', 'General'), ('deployment', 'Deployment'), ('maintenance', 'Maintenance')])


class UserRoleForm(Form):
    """Form for assigning roles to an User"""
    user = SelectField(label='User', coerce=str)
    roles = MultiCheckboxField(label='Roles', coerce=str)


class ServerMachineAddForm(Form):
    """Form for adding new server"""
    host_name = StringField(label='Host Name')
    host_ip = StringField(label='Host IP Address', validators=[validators.IPAddress(), validators.data_required])
    host_address = StringField(label='Host Address', validators=[validators.data_required])
    ssh_username = StringField(label='SSH Username', validators=[validators.data_required])
    ssh_password = PasswordField(label='SSH Password', validators=[validators.data_required])
    ssh_port = IntegerField(label='SSH Port', validators=[validators.data_required])
    mysql_username = StringField(label='MySQL Username', validators=[validators.data_required])
    mysql_password = PasswordField(label='MySQL Password', validators=[validators.data_required])