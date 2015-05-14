__author__ = 'HZ'

from tasks import *


###########################################################################
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
        pass
        #put Core4 or other type product deploy system here
        #task = long_task.apply_async([request.form['project_id']])

    #insert the celery task id in db of project for future reference
    project = Project.query.get(request.form['project_id'])
    project.celery_task_id = task.id
    db.session.commit()

    #return empty data, status, and request header to ajaj
    return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}


###########################################################################
# Get ajaj response of the current long running task
@app.route('/status/<task_id>')
@login_required
@roles_accepted('admin', 'mod')
def taskstatus(task_id):
    task = PrismERPDeploy.AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    # All except failure....
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.info.get('status', ''),
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
            response['log'] = task.info['log']
        if 'cmd' in task.info:
            #print 'cmd out here', task.info
            response['cmd'] = task.info['cmd']
            response['output'] = task.info['output']

    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


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