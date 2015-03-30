__author__ = 'HZ'


from flask_wtf import Form
from wtforms import StringField, SubmitField, validators


class CmdExecuteForm(Form):
    cmd = StringField(validators=[validators.data_required])


class TaskExecuteForm(Form):
    cmd = StringField(validators=[validators.data_required])
    params = StringField()
    switches = StringField()
    arguments = StringField()