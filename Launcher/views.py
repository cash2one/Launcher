__author__ = 'HZ'

from .import app, db, celery, session
from flask import render_template, flash, request, redirect, url_for, jsonify

from flask_user import current_user, login_required
#from forms import UserProfileForm

from formalchemy import FieldSet
from models import *


############################################################################
# Dummy route for testing site layout for dev purpose
@app.route('/preview')
def test():
    return render_template('base.html')


############################################################################
# Site root, Index view, Dashboard
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
#@login_required
def index():

    return render_template('index.html')


# ###########################################################################
# List of all projects with info from database
@app.route('/projects_list')
def projects_list():

    projects = Project.query.all()

    return render_template('projects/projects_list.html', projects=projects)


# ###########################################################################
# Add a new project, possibly for future deploy
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
        #fs.is_deployed.hidden(),
        #fs.celery_task_id.hidden()
    ])

    if request.method == 'POST':
        fs.rebind(data=request.form)
        if fs.validate():
            fs.sync()
            db.session.add(project)
            db.session.commit()
            flash('Project successfully added!')

    fs.rebind(model=Project)

    return render_template('projects/project_add.html', form=fs)


# ###########################################################################
# List of projects with status and action button to deploy or maintain
@app.route('/deploy_a_project/')
def deploy_project_list():
    projects = Project.query.all()

    return render_template('projects/project_deploy_list.html', projects=projects)


# ###########################################################################
# Deploy a project, takes confirmation and move to actual deploy phase, all magic here
@app.route('/project_detail/<project_id>')
def deploy_project(project_id):

    project = Project.query.get(project_id)
    task_id = project.celery_task_id

    celery_task = long_task.AsyncResult(task_id)

    if task_id:
        project_status = celery_task.state
    else:
        project_status = ''


    print celery_task, celery_task.state, celery_task.info

    return render_template('projects/project_detail.html', project=project, project_status=project_status)


# ###########################################################################
# List of all software products
@app.route('/products_list')
def products_list():

    products = Product.query.all()

    return render_template('products/products_list.html', products=products)


# ###########################################################################
# Add a new software solution that was made
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

    return render_template('products/product_add.html', form=fs)


# ###########################################################################
# List of all tasks added by Super Admin under careful consideration
@app.route('/task_list')
def task_list():

    tasks = Task.query.all()

    return render_template('tasks/task_list.html', tasks=tasks)


# ###########################################################################
# Add a new task command to be executed, added by only Supreme Admin by careful planning
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

    return render_template('tasks/task_add.html', form=fs)


# ###########################################################################
# Execute a task command directly on shell, only by Supreme Admin
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

    return render_template('tasks/shell.html', cmd=cmd, out=out, form=form)


# ###########################################################################
# Gets the detail of a task process ongoing
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

    return render_template('tasks/task_detail.html', task=task, form=form)


# ###########################################################################
# List of all registered users of the web app
@app.route('/users_list')
def users_list():
    return ''


# ###########################################################################
# Add a new user, manually by Super Admin
@app.route('/user_add')
def user_add():
    return ''


# ###########################################################################
# List of all server host machines, viewable by only authenticated users
@app.route('/hosts_list')
def hosts_list():

    hosts = Machine.query.all()

    return render_template('hosts/hosts_list.html', hosts=hosts)


# ###########################################################################
# Add a new server host machine, manually
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

            return redirect(url_for('hosts_list'))

    fs.rebind(model=Machine)

    return render_template('hosts/host_add.html', form=fs)


# ###########################################################################
# View profile, self or other members
@app.route('/profile_view')
def profile_view():
    return ''


# ###########################################################################
# Edit own profile
@app.route('/profile_edit')
def profile_edit():
    return ''


# ###########################################################################
# Makes a shell command based on options added to the database
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


# ###########################################################################
# Test ajaj view
@app.route('/send')
def ajaj():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)

    return jsonify(res=a + b)


# ###########################################################################
# Prism ERP deploy procedure
@app.route('/prism_deploy')
def PrismERPDeploy():

    # import fabfile
    #
    # fabfile.tasks.LocalDeployment.checkout()
    # fabfile.tasks.LocalDeployment.change_static_to_pro()
    # fabfile.tasks.LocalDeployment.create_vhost()
    print request.args
    project_id = request.args.get('project_id')
    project = Project.query.get(project_id)

    return jsonify({})


# ###########################################################################
# Execute a task and return ajaj reponse
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

############################################################################
# Implementing Celery
# Starts by Initiating the long celery task
@app.route('/longtask', methods=['POST'])
def longtask():

    #start the async celery task
    task = long_task.apply_async()

    #insert the celery task id in db of project for future reference
    project = Project.query.get(request.form['project_id'])
    project.celery_task_id = task.id
    db.session.commit()

    #return empty data, status, and request header to ajaj
    return jsonify({}), 202, {'Location': url_for('taskstatus',task_id=task.id)}


# Get ajaj response of the current long running task
@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


# The CELERY LONG TASK
@celery.task(bind=True)
def long_task(self):
    import random, time, threading
    """Background task that runs a long function with progress reports."""

    message = ''

    t = threading.Thread(target=f)
    t.start()

    while t.isAlive():
        self.update_state(state='PROGRESS', meta={'status': 'Deployment in progress....'})


    return {'status': 'Task Completed!', 'result': 'Project Deployment Completed!'}


# Test function for celery
def f():
    from fabric.api import local
    out = local('ping google.com', True)


