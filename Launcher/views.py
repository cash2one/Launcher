__author__ = 'HZ'

from .import app, db, celery_obj, security, mail
from flask import render_template, flash, request, redirect, url_for, jsonify, session

from formalchemy import FieldSet
from models import *

from flask.ext.security import login_required, roles_required, roles_accepted, current_user, url_for_security


############################################################################
@app.route('/preview')
@login_required
def test():
    """Dummy route for testing site layout for dev purpose"""
    if current_user:
        print current_user.email
    return render_template('base.html')


############################################################################
@app.route('/')
@app.route('/index')
#@login_required
def index():
    """Site root, Index view, Dashboard"""
    return render_template('index.html')


############################################################################
@app.route('/projects_list')
#@roles_required('mod')
@login_required
def projects_list():
    """List of all projects with info from database"""
    projects = Project.query.all()

    return render_template('projects/projects_list.html', projects=projects)


###########################################################################
@app.route('/project_add', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'mod')
def project_add():
    """Add a new project, possibly for future deploy"""
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


###########################################################################
@app.route('/deploy_a_project/')
@login_required
@roles_accepted('admin', 'mod')
def deploy_project_list():
    """List of projects with status and action button to deploy or maintain"""
    projects = Project.query.all()

    return render_template('projects/project_deploy_list.html', projects=projects)


###########################################################################
@app.route('/project_detail/<project_id>')
@login_required
@roles_accepted('admin', 'mod')
def deploy_project(project_id):
    """Deploy a project, takes confirmation and move to actual deploy phase, all magic here"""
    import requests, json
    api_root = 'http://localhost:5555/api'
    task_api = '{}/task'.format(api_root)
    task_info_api = '{}/info'.format(task_api)

    project = Project.query.get(project_id)
    task_id = project.celery_task_id

    if project.is_deployed:
        project_status = 'SUCCESS'

    elif task_id:
        #project deploy process started before...chk the current status
        url = task_info_api + '/{}'.format(task_id)
        response = requests.get(url)
        if response.content:
            result = json.loads(response.content)
            project_status = result['state']
            print project_status
        else:
            #no info against task_id means it was abrupted
            project_status = 'HAULTED'
            print 'Project Deployment task not present in celery...celery was restarted....chk project_deployed status.'

    else:
        # Page may have been visited but deploy button not click even once...ergo deployment process never started
        project_status = 'WAITING'


    return render_template('projects/project_detail.html', project=project, project_status=project_status)


###########################################################################
@app.route('/products_list')
@login_required
def products_list():
    """List of all software products"""
    products = Product.query.all()

    return render_template('products/products_list.html', products=products)


###########################################################################
@app.route('/product_add', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'mod')
def product_add():
    """Add a new software solution that was made"""
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


###########################################################################
@app.route('/task_list')
@login_required
def task_list():
    """List of all tasks added by Super Admin under careful consideration"""
    tasks = Task.query.all()

    return render_template('tasks/task_list.html', tasks=tasks)


###########################################################################
@app.route('/task_add', methods=['GET','POST'])
@login_required
@roles_accepted('admin', 'mod')
def task_add():
    """Add a new task command to be executed, added by only Supreme Admin by careful planning"""
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


###########################################################################
@app.route('/cmd_execute', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def cmd_execute():
    """Execute a task command directly on shell, only by Supreme Admin"""
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


###########################################################################
@app.route('/task_detail/<task_id>', methods=['GET','POST'])
@login_required
@roles_accepted('admin')
def task_detail(task_id):
    """Gets the detail of a task process ongoing"""
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


###########################################################################
@app.route('/users_list')
@login_required
def users_list():
    """List of all registered users of the web app"""
    return ''


###########################################################################
@app.route('/user_add')
@login_required
@roles_accepted('admin', 'mod')
def user_add():
    """Add a new user, manually by Super Admin"""
    return ''


###########################################################################
@app.route('/hosts_list')
@login_required
@roles_accepted('admin', 'mod')
def hosts_list():
    """List of all server host machines, viewable by only authenticated users"""
    hosts = Machine.query.all()

    return render_template('hosts/hosts_list.html', hosts=hosts)


###########################################################################
@app.route('/host_add', methods=['GET','POST'])
@login_required
@roles_accepted('admin', 'mod')
def host_add():
    """Add a new server host machine, manually"""
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


###########################################################################
@app.route('/profile_view')
@login_required
def profile_view():
    """View profile, self or other members"""
    return ''


###########################################################################
@app.route('/profile_edit')
@login_required
def profile_edit():
    """Edit own profile"""
    return ''


###########################################################################
def make_command(command='', parameters=[], switches=[], arguments=[]):
    """Makes a shell command based on options added to the database"""
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


###########################################################################
@app.route('/task_execute')
@login_required
@roles_accepted('admin', 'mod')
def task_execute():
    """Execute a task and return ajaj reponse"""
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
@login_required
@roles_accepted('admin', 'mod')
def longtask():

    #start the async celery task
    if request.form['project_type'] == 'PrismERP':
        task = PrismERPDeploy.apply_async([request.form['project_id']])
    else:
        task = long_task.apply_async([request.form['project_id']])

    #insert the celery task id in db of project for future reference
    project = Project.query.get(request.form['project_id'])
    project.celery_task_id = task.id
    db.session.commit()

    #return empty data, status, and request header to ajaj
    return jsonify({}), 202, {'Location': url_for('taskstatus',task_id=task.id)}


# Get ajaj response of the current long running task
@app.route('/status/<task_id>')
@login_required
@roles_accepted('admin', 'mod')
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
@celery_obj.task(bind=True)
def long_task(self, project_id):
    import random, time, threading
    """Background task that runs a long function with progress reports."""

    message = ''
    project = Project.query.get(project_id)

    t = threading.Thread(target=f)
    t.start()

    while t.isAlive():
        self.update_state(state='INITIAL', meta={'status': 'Deployment in progress....'})


    return {'status': 'Task Completed!', 'result': 'Project Deployment Completed!'}


# Test function for celery
def f():
    from fabric.api import local
    out = local('ping google.com', True)


# ###########################################################################
# Prism ERP deploy procedure
@celery_obj.task(bind=True)
def PrismERPDeploy(self, project_id):

    import threading, time, os, random
    from fabfile.fabfile import local_deploy

    project = Project.query.get(project_id)
    tasks = [
        #['CheckOut', local_deploy.checkout],
        ['Static File Minification', local_deploy.change_static_to_pro],
        #['Database Creation', local_deploy.create_db],
        ['Deployment Setting Change', local_deploy.change_settings]
    ]

    completed_tasks = 0

    #Dummy Steps
    self.update_state(state='INITIAL', meta={'status': 'Preparing to deploy......'})
    time.sleep(4)
    self.update_state(state='INITIAL', meta={'status': 'Gathering resources......'})
    time.sleep(4)

    sql_paths = [
        os.path.join(project.project_dir, 'database', 'prism.sql'),
        os.path.join(project.project_dir, 'database', 'sphere.sql'),
        os.path.join(project.project_dir, 'database', 'lines.sql')
    ]

    changes_dict = {
        'INTERNAL_NAME': '\'prism\'',
        'PRODUCT_NAME': '\'Sphere\'',
        'PRODUCT_TITLE': '\'Lines\'',
        'DEBUG': 'False',
        'PRODUCTION': 'True',
        # 'DIVINEMAIL_IP' : '',
        '\'NAME\':': '\'testdb\',',
        '\'USER\':': '\'HUZR\',',
        '\'PASSWORD\':': '\'123\',',
        'BIRTVIEWER_DIR': '\'D:\\\\birt\\\\\'',
        'COMPANY_NAME': '\'HZ\''
    }

    args_list = [
        #[project.vcs_repo, project.project_dir],
        [os.path.join(project.project_dir, 'public', 'static')],
        #[project.mysql_db_name, sql_paths],
        [project.project_dir, changes_dict]
    ]

    for i in range(len(tasks)):
        t = threading.Thread(target=tasks[i][1], args=args_list[i])
        current_task = tasks[i][0]
        phrases = [
            'Completed: {}/{} tasks'.format(str(completed_tasks), str(len(tasks))),
            'Executing Task: {}.....'.format(current_task),
            'Project Deployment in progress at step {}....'.format(str(i + 1))
        ]

        t.start()

        while t.isAlive():

            self.update_state(
                state='PROGRESS',
                meta={
                    'status': random.choice(phrases)
                }
            )

        completed_tasks += 1

        self.update_state(
            state='PROGRESS',
            meta={
                'status': phrases[0]
            }
        )

        time.sleep(4)

    project.is_deployed = 1
    db.session.commit()

    return {'status': 'All Tasks Completed!', 'result': 'Project Deployment Completed!'}

# Setup the task
@celery_obj.task
def send_security_email(msg):
    # Use the Flask-Mail extension instance to send the incoming ``msg`` parameter
    # which is an instance of `flask_mail.Message`
    mail.send(msg)

@security.send_mail_task
def delay_security_email(msg):
    send_security_email.delay(msg)