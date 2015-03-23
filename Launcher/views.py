__author__ = 'HZ'

from .import app, db
from flask import render_template, flash, request, redirect, url_for

from flask_user import current_user, login_required
#from forms import UserProfileForm

@app.route('/preview')
def test():
    return render_template('base.html')



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
#@login_required
def index():

    return render_template('index.html')


@app.route('/projects_list')
def projects_list():

    from models import Project

    projects = Project.query.all()

    return render_template('projects_list.html', projects=projects)


@app.route('/project_add')
def project_add():

    from formalchemy import FieldSet
    from models import Project, Product

    project = Project()
    fs = FieldSet(project)

    # stage_options = [('', ''), ('Deployment', 'Deployment'), ('Maintenance', 'Maintenance'), ('General', 'General')]
    # # route_type_options = {'one':'1','two':'2','three':'3'}
    # fs.configure(options=[
    #     fs.name.label('Task Name'),
    #     fs.cmd.label('Command'),
    #     fs.params.label('Parameters'),
    #     fs.stage.dropdown(
    #         stage_options
    #     )
    # ]
    # )
    product_options = [(each[0], each[0]) for each in Product.query.with_entities(Product.name).all()]

    fs.configure(options=[
        fs.product_type.dropdown(product_options)
    ])

    if request.method == 'POST':
        fs.rebind(data=request.form)
        if fs.validate():
            fs.sync()
            db.session.add(project)
            db.session.commit()

    fs.rebind(model=Project)

    return render_template('project_add.html', form=fs)


@app.route('/products_list')
def products_list():

    from models import Product

    products = Product.query.all()

    return render_template('products_list.html', products=products)


@app.route('/product_add')
def product_add():
    return ''


@app.route('/task_list')
def task_list():
    from models import Task
    tasks = Task.query.all()

    return render_template('task_list.html', tasks=tasks)


@app.route('/task_add', methods=['GET','POST'])
def task_add():

    from models import Task
    from formalchemy import FieldSet
    task = Task()
    fs = FieldSet(task)

    stage_options = [('', ''), ('Deployment', 'Deployment'), ('Maintenance', 'Maintenance'), ('General', 'General')]
    # route_type_options = {'one':'1','two':'2','three':'3'}
    fs.configure(options=[
        fs.name.label('Task Name'),
        fs.cmd.label('Command'),
        fs.params.label('Parameters'),
        fs.stage.dropdown(
            stage_options
        )
    ]
    )

    if request.method == 'POST':
        fs.rebind(data=request.form)
        if fs.validate():
            fs.sync()
            db.session.add(task)
            db.session.commit()

    fs.rebind(model=Task)

    return render_template('task_add.html', form=fs)


@app.route('/cmd_execute', methods=['GET', 'POST'])
def cmd_execute():
    from models import Task
    #from flask_sqlalchemy import SQLAlchemy
    from fabric.api import local
    from forms import CmdExecuteForm

    from models import Task

    task = Task.query.get(3)
    c = task.cmd
    p = ''
    if task.params is not None:
        for each in task.params.split(','):
            p += str(each) + ' '
    s = ''
    if task.switches is not None:
        for each in task.switches.split(','):
            s += str(each) + ' '
    a = ''
    if task.arguments is not None:
        for each in task.arguments.split(','):
            a += str(each) + ' '

    print ' '.join([c,p,s,a])


    form = CmdExecuteForm()

    if request.method == 'GET' and request.args:

        cmd = request.args['cmd']
        print cmd
        try:
            out = local(cmd, True)
        except SystemExit:
            flash("Invalid Command")
            out = 'Please enter a valid command!'

    elif request.method == 'POST':

        cmd = request.form['cmd']
        print cmd
        try:
            out = local(cmd, True)
        except SystemExit:
            flash("Invalid Command")
            out = 'Please enter a valid command!'
    else:
        cmd = 'Enter a command!'
        out = 'None'

    return render_template('shell.html', cmd=cmd, out=out, form=form)


@app.route('/task_execute', methods=['GET','POST'])
def task_execute():

    return ''

@app.route('/task_detail/<task_id>', methods=['GET','POST'])
def task_detail(task_id):
    from models import Task
    task = Task.query.get(task_id)

    from flask_wtf import Form
    from wtforms import StringField, SubmitField, validators, FieldList, FormField

    class TaskExcForm(Form):
        pass

    if task.params:
        for each in task.params.split(','):
            setattr(TaskExcForm, each, StringField())
    if task.arguments:
        for each in task.arguments.split(','):
            setattr(TaskExcForm, each, StringField())

    form=TaskExcForm()

    if request.method == 'POST':
        #print request.form
        kw = ''
        for each in request.form:
            if not each == 'csrf_token':
                if task.params and each in task.params.split(','):
                    kw += each + ' ' + request.form[each]
                elif task.arguments and each in task.arguments.split(','):
                    kw += request.form[each] + ' '

        c = task.cmd
        if task.switches:
            s = task.switches
        else:
            s = ''
        cmd = ' '.join([c, kw, s])
        print cmd
        return redirect(url_for('cmd_execute', cmd=cmd))

    return render_template('task_detail.html', task=task, form=form)


@app.route('/users_list')
def users_list():
    return ''


@app.route('/user_add')
def user_add():
    return ''


@app.route('/hosts_list')
def hosts_list():

    from models import Machine

    hosts = Machine.query.all()



    return render_template('hosts_list.html', hosts=hosts)


@app.route('/host_add')
def host_add():
    return ''


@app.route('/profile_view')
def profile_view():
    return ''


@app.route('/profile_edit')
def profile_edit():
    return ''