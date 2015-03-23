__author__ = 'HZ'

from .import app, db
from flask import render_template, flash, request, redirect, url_for, jsonify

from flask_user import current_user, login_required
#from forms import UserProfileForm

from formalchemy import FieldSet
from models import *

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

    projects = Project.query.all()

    return render_template('projects_list.html', projects=projects)


@app.route('/project_add', methods=['GET', 'POST'])
def project_add():

    project = Project()
    fs = FieldSet(project)

    product_options = [('','')]
    servers = [('',''), ('Local', 'Local')]

    for each in Product.query.with_entities(Product.name).all():
        product_options.append((each[0], each[0]))

    for each in Machine.query.with_entities(Machine.id,Machine.host_name).all():
        servers.append((each[1], str(each[0])))

    vcs = [('SVN', 'SVN'), ('Git', 'Git')]

    fs.configure(options=[
        fs.product_type.dropdown(product_options),
        fs.server_id.label('Server Machine').dropdown(servers),
        fs.vcs_tool.label('Version Control').dropdown(vcs)
    ])

    if request.method == 'POST':
        fs.rebind(data=request.form)
        if fs.validate():
            fs.sync()
            db.session.add(project)
            db.session.commit()
            flash('Project successfully added!')

    fs.rebind(model=Project)

    return render_template('project_add.html', form=fs)


@app.route('/deploy_project/')
def deploy_project_list():
    projects = Project.query.all()

    return render_template('project_deploy_list.html', projects=projects)


@app.route('/deploy_project/<project_id>')
def deploy_project(project_id):
    project = Project.query.get(project_id)

    return render_template('project_deploy.html', project=project)


@app.route('/products_list')
def products_list():

    products = Product.query.all()

    return render_template('products_list.html', products=products)


@app.route('/product_add', methods=['GET', 'POST'])
def product_add():

    product = Product()
    fs = FieldSet(product)

    languages = [('Python', 'Python'), ('PHP', 'PHP'), ('Perl', 'Perl'), ('Ruby', 'Ruby'), ('Java', 'Java')]
    frameworks = [('FurinaPy', 'FurinaPy'), ('FurinaPHP', 'FurinaPHP'), ('django', 'django'), ('Flask', 'Flask'), ('Pyramid', 'Pyramid'), ('Bottle', 'Bottle'), ('Web2Py', 'Web2Py'), ('Cake', 'Cake')]

    fs.configure(options=[
        fs.language.dropdown(languages),
        fs.framework.dropdown(frameworks)
    ])

    if request.method == 'POST':
        fs.rebind(data=request.form)
        if fs.validate():
            fs.sync()
            db.session.add(product)
            db.session.commit()
            flash('Product successfully added!')

    fs.rebind(model=Product)

    return render_template('product_add.html', form=fs)


@app.route('/task_list')
def task_list():

    tasks = Task.query.all()

    return render_template('task_list.html', tasks=tasks)


@app.route('/task_add', methods=['GET','POST'])
def task_add():

    task = Task()
    fs = FieldSet(task)

    stage_options = [('', ''), ('Deployment', 'Deployment'), ('Maintenance', 'Maintenance'), ('General', 'General')]
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
            flash('Task successfully added!')

    fs.rebind(model=Task)

    return render_template('task_add.html', form=fs)


@app.route('/cmd_execute', methods=['GET', 'POST'])
def cmd_execute():

    from fabric.api import local
    from forms import CmdExecuteForm

    form = CmdExecuteForm()

    if request.method == 'GET' and request.args:

        cmd = request.args['cmd']
        #print cmd
        try:
            out = local(cmd, True)

        except SystemExit:
            flash("Invalid Command")
            out = 'Please enter a valid command!'

    elif request.method == 'POST':

        cmd = request.form['cmd']
        #print cmd
        try:
            out = local(cmd, True)
        except SystemExit:
            flash("Invalid Command")
            out = 'Please enter a valid command!'
    else:
        cmd = 'Enter a command!'
        out = 'None'

    return render_template('shell.html', cmd=cmd, out=out, form=form)


@app.route('/task_detail/<task_id>', methods=['GET','POST'])
def task_detail(task_id):

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

        parameters = []
        switches = []
        arguments = []

        if task.params:
            for each in task.params.split(','):
                parameters.append((each, request.form[each]))
        if task.arguments:
            for each in task.arguments.split(','):
                arguments.append((each,request.form[each]))

        if task.switches:
            for each in task.switches.split(','):
                switches.append(each)

        #print 'Command: %s' %make_command(command=task.cmd, parameters=parameters, switches=switches, arguments=arguments)
        cmd = make_command(command=task.cmd, parameters=parameters, switches=switches, arguments=arguments)

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

    hosts = Machine.query.all()

    return render_template('hosts_list.html', hosts=hosts)


@app.route('/host_add', methods=['GET','POST'])
def host_add():

    machine = Machine()
    fs = FieldSet(machine)

    if request.method == 'POST':
        fs.rebind(data=request.form)
        if fs.validate():
            fs.sync()
            db.session.add(machine)
            db.session.commit()
            flash('Server successfully added!')

    fs.rebind(model=Machine)

    return render_template('host_add.html', form=fs)


@app.route('/profile_view')
def profile_view():
    return ''


@app.route('/profile_edit')
def profile_edit():
    return ''



def make_command(command='', parameters=[], switches=[], arguments=[]):

    print command, parameters, switches, arguments

    cmd = command

    para = ''
    if parameters:
        for each in parameters:
            if each[1]:
                para += ' ' + str(each[0]) + ' ' + str(each[1])

    sw = ''
    if switches:
        for each in switches:
            sw += str(each) + ' '

    args = ''
    if arguments:
        for each in arguments:
            if each[1]:
                args += str(each[1]) + ' '

    if para:
        cmd += para
    if sw:
        cmd += ' ' + sw
    if args:
        cmd += ' ' + args

    print "Command is: %s" %cmd

    return cmd


@app.route('/send')
def ajaj():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)

    return jsonify(res=a + b)


def PrismDeploy():
    import fabfile

    #fabfile.tasks.LocalDeployment.deploy_project()


@app.route('/task_execute')
def task_execute():
    from fabric.api import local

    if request.method == 'GET' and request.args:

        cmd = request.args['cmd']

        try:
            out = local(cmd, True)

        except SystemExit:
            flash("Invalid Command")
            out = 'Please enter a valid command!'

    elif request.method == 'POST':

        cmd = request.form['cmd']

        try:
            out = local(cmd, True)
        except SystemExit:
            flash("Invalid Command")
            out = 'Please enter a valid command!'
    else:
        cmd = 'Enter a command!'
        out = 'None'

    return jsonify(cmd=cmd, output=out.split('\n'))