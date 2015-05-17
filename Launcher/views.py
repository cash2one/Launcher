__author__ = 'HZ'

from .import app, db, celery_obj, security, mail, user_datastore
from flask import render_template, flash, request, redirect, url_for, jsonify, session, abort

from formalchemy import FieldSet
from models import *
from forms import *

from flask.ext.security import login_required, roles_required, roles_accepted, current_user, url_for_security

from utils import DST


################################--Homepage--################################
############################################################################
@app.route('/')
@app.route('/index')
def index():
    """Site root, Index view, Dashboard"""
    #Includes the short 'HowTo'
    return render_template('index.html')


############################---Projects Views---############################
############################################################################
@app.route('/projects_list')
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

    project_add_form = ProjectAddEditForm(formdata=request.form)
    project_add_form.product_type.choices = [(each[0], each[0]) for each in Product.query.with_entities(Product.name).all()]
    project_add_form.server_id.choices = [(each[1], each[0]) for each in Machine.query.with_entities(Machine.host_name, Machine.id).all()]

    if request.method == 'POST':
        if project_add_form.validate_on_submit():
            project = Project()
            project_add_form.populate_obj(obj=project)
            db.session.add(project)
            db.session.commit()
            flash('Project Successfully Added!')
            return redirect(url_for('projects_list'))
        else:
            flash('Form Validation Failed!!')

    return render_template('projects/project_add.html', form=project_add_form)


###########################################################################
@app.route('/project_edit/<project_id>', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'mod')
def project_edit(project_id):
    """Edit a project information"""

    project = Project.query.get_or_404(project_id)

    project_edit_form = ProjectAddEditForm(formdata=request.form, obj=project)
    project_edit_form.product_type.choices = [(each[0], each[0]) for each in Product.query.with_entities(Product.name).all()]
    project_edit_form.server_id.choices = [(each[1], each[0]) for each in Machine.query.with_entities(Machine.host_name, Machine.id).all()]

    if request.method == 'POST':
        if project_edit_form.validate_on_submit():
            project_edit_form.populate_obj(obj=project)
            db.session.commit()
            flash('Project Successfully Edited!')
            return redirect(url_for('projects_list'))
        else:
            flash('Form Validation Failed!!')

    return render_template('projects/project_edit.html', form=project_edit_form, project=project)


###########################################################################
@app.route('/project_delete/<project_id>', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def project_delete(project_id):
    """Delete a project from the database"""

    project = Project.query.get_or_404(project_id)

    if request.is_xhr:
        db.session.delete(project)
        db.session.commit()
        flash('Project Deleted Successfully!')

    return render_template('projects/project_delete.html', project=project)


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
    from tasks import PrismERPDeploy
    #import requests, json
    #api_root = 'http://localhost:5555/api'
    #task_api = '{}/task'.format(api_root)
    #task_info_api = '{}/info'.format(task_api)

    project = Project.query.get(project_id)
    task_id = project.celery_task_id

    if project.is_deployed:
        project_status = 'SUCCESS'

    elif task_id:
        task = PrismERPDeploy.AsyncResult(task_id)
        #project deploy process started before...chk the current status
        #url = task_info_api + '/{}'.format(task_id)
        #response = requests.get(url)
        response = task.status
        if response:
            #result = json.loads(response.content)
            #project_status = result['state']
            project_status = response
            print project_status
        else:
            #no info against task_id means it was abrupted
            project_status = 'HAULTED'
            print 'Project Deployment task not present in celery...celery was restarted....chk project_deployed status.'

    else:
        # Page may have been visited but deploy button not click even once...ergo deployment process never started
        project_status = 'WAITING'


    return render_template('projects/project_detail.html', project=project, project_status=project_status)


#########################----Product Views----#############################
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

    product_add_form = ProductAddEditForm(request.form)

    if request.method == 'POST':
        if product_add_form.validate_on_submit():
            product = Product()
            product_add_form.populate_obj(product)
            db.session.add(product)
            db.session.commit()
            flash('New Product Added Successfully!')
            return redirect(url_for('products_list'))

    return render_template('products/product_add.html', form=product_add_form)


###########################################################################
@app.route('/product_edit/<product_id>', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def product_edit(product_id):
    """Edit a product from the database"""

    product = Product.query.get_or_404(product_id)

    product_edit_form = ProductAddEditForm(request.form, product)

    if request.method == 'POST':
        if product_edit_form.validate_on_submit():
            product_edit_form.populate_obj(product)
            db.session.commit()
            flash('Product Edited Successfully!')
            return redirect(url_for('products_list'))
        else:
            flash('Form Validaion Failed!!')

    return render_template('products/product_edit.html', form=product_edit_form, product=product)


###########################################################################
@app.route('/product_delete/<product_id>', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def product_delete(product_id):
    """Delete a product from the database"""

    product = Product.query.get_or_404(product_id)

    if request.is_xhr:
        db.session.delete(product)
        db.session.commit()
        flash('Product Deleted Successfully!')

    return render_template('products/product_delete.html', product=product)


#########################-----Tasks Views-----#############################
###########################################################################
@app.route('/task_list')
@login_required
def task_list():
    """List of all tasks added by Super Admin under careful consideration"""
    tasks = Task.query.all()

    return render_template('tasks/task_list.html', tasks=tasks)


###########################################################################
@app.route('/task_add', methods=['GET', 'POST'])
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
@app.route('/task_detail/<task_id>', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def task_detail(task_id):
    """Gets the detail of a task process ongoing"""
    task = Task.query.get(task_id)

    from flask_wtf import Form
    from wtforms import StringField, SubmitField, validators, FieldList, FormField
    from utils import make_command

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


#########################-----User Views----###############################
###########################################################################
@app.route('/users_list')
@login_required
def users_list():
    """List of all registered users of the web app"""
    users = User.query.all()

    return render_template('users/user_list.html', users=users)


###########################################################################
@app.route('/user_role_assign', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'mod')
def user_role_assign():
    """Add a new user role, manually by Super Admin"""
    user_role_form = UserRoleForm(request.form)

    users = User.query.all()
    roles = Role.query.all()
    user_opts = [(each.email, each.email) for each in users]
    roles_opts = [(each.name, each.description) for each in roles]

    user_role_form.user.choices = user_opts
    user_role_form.roles.choices = roles_opts

    if request.method == 'POST':
        if user_role_form.validate_on_submit():
            roles = user_role_form.roles.data
            for each in roles:
                user = user_datastore.find_user(email=user_role_form.user.data)
                role = user_datastore.find_role(each)
                result = user_datastore.add_role_to_user(user, role)

            db.session.commit()

            flash('Successfully assigned Roles to the User: ' + user_role_form.user.data)
            return redirect(url_for('user_role_assign'))
        else:
            flash('Form Validation Failed!')

    return render_template('users/userrole.html', form=user_role_form)


# ##########################################################################
@app.route('/user_role_create', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def user_role_create():
    """Add a new role, manually by Super Admin"""
    role_create_form = RoleCreateForm(request.form)

    if request.method == 'POST':
        if role_create_form.validate_on_submit():
            role_name = role_create_form.name.data
            role_description = role_create_form.description.data

            user_datastore.create_role(name=role_name, description=role_description)
            db.session.commit()

            flash('Successfully created the role...now it can be assigned to users.')
            return redirect(url_for('user_role_create'))
        else:
            flash('Form Validation Failed!')

    return render_template('users/role_create.html', form=role_create_form)


#######################-----Servers Views----##############################
###########################################################################
@app.route('/hosts_list')
@login_required
@roles_accepted('admin', 'mod')
def hosts_list():
    """List of all server host machines, viewable by only authenticated users"""

    hosts = Machine.query.all()

    return render_template('hosts/hosts_list.html', hosts=hosts)


###########################################################################
@app.route('/host_add', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'mod')
def host_add():
    """Add a new server host machine, manually"""

    host_add_form = ServerMachineAddEditForm(request.form)

    if request.method == 'POST':
        if host_add_form.validate_on_submit():
            host = Machine()
            host_add_form.populate_obj(host)

            db.session.add(host)
            db.session.commit()
            flash('New Server Added Successfully!')
            return redirect(url_for('hosts_list'))

    return render_template('hosts/host_add.html', form=host_add_form)


###########################################################################
@app.route('/host_edit/<machine_id>', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'mod')
def host_edit(machine_id):
    """Add a new server host machine, manually"""

    host = Machine.query.get_or_404(machine_id)
    host.ssh_password = pwd_decryption(host.ssh_password)
    host.db_password = pwd_decryption(host.db_password)

    host_edit_form = ServerMachineAddEditForm(formdata=request.form, obj=host)

    if request.method == 'POST':
        if host_edit_form.validate_on_submit():
            host_edit_form.populate_obj(host)
            db.session.commit()
            flash('Server Edited Successfully!')
            return redirect(url_for('hosts_list'))

    return render_template('hosts/host_edit.html', form=host_edit_form, host=host)


###########################################################################
@app.route('/host_delete/<machine_id>', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def host_delete(machine_id):
    """Delete a project from the database"""

    host = Machine.query.get_or_404(machine_id)

    if request.is_xhr:
        db.session.delete(host)
        db.session.commit()
        flash('Server Deleted Successfully!')

    return render_template('hosts/host_delete.html', host=host)


#######################-----Setting Views----##############################
###########################################################################
@app.route('/profile_view')
@login_required
def profile_view():
    """View profile, self or other members"""
    user = User.query.get(current_user.id)
    #msgs = user.msgs_received

    return render_template('users/profile_view.html', user=user, DST=DST)


###########################################################################
@app.route('/profile_edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    """Edit own profile"""

    user = User.query.get_or_404(current_user.id)
    user.svn_password = pwd_decryption(user.svn_password)

    profile_edit_form = ProfileEditForm(formdata=request.form, obj=user)

    if request.method == 'POST':
        if profile_edit_form.validate_on_submit():
            profile_edit_form.populate_obj(user)
            db.session.commit()
            flash('Successfully updated profile info!')
            return redirect(url_for('profile_view'))
        else:
            flash('Form Validation Failed!!')

    return render_template('users/profile_edit.html', user=user, DST=DST, form=profile_edit_form)


###########################################################################

@app.route('/message', methods=['GET', 'POST'])
@login_required
def messages():

    if request.is_xhr:
        msg = Message.query.get(request.form['msg_id'])
        data = dict()
        data['msg_id'] = msg.id
        data['sender'] = msg.owner.first().email
        data['receiver'] = msg.receipient.first().email
        data['msg-body'] = msg.message_body
        data['date'] = msg.sent_at

        if not msg.owner.first().id == current_user.id and not msg.read:
            msg.read = 1
            db.session.commit()
            data['seen'] = True

        return jsonify(data)

    return render_template('users/messages.html')