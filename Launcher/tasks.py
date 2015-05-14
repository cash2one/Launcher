__author__ = 'HZ'

from views import *


# Async Email sending
# Setup the task
@celery_obj.task
def send_security_email(msg):
    # Use the Flask-Mail extension instance to send the incoming ``msg`` parameter
    # which is an instance of `flask_mail.Message`
    with app.app_context():
        mail.send(msg)


@security.send_mail_task
def delay_security_email(msg):
    send_security_email.delay(msg)


# Test function for celery
def f():
    from fabric.api import local
    out = local('ping google.com', True)

# The CELERY LONG TASK Test
@celery_obj.task(bind=True)
def long_task(self, project_id):
    import random, time, threading
    """Background task that runs a long function with progress reports."""

    t = threading.Thread(target=f)
    t.start()

    while t.isAlive():
        self.update_state(state='INITIAL', meta={'status': 'Deployment in progress....'})

    return {'status': 'Task Completed!', 'result': 'Project Deployment Completed!'}


# ###########################################################################
# Prism ERP deploy procedure test
@celery_obj.task(bind=True)
def localPrismERPDeploy(self, project_id):

    import threading, time, os, random, Queue
    from fabfile.fabfile import local_deploy

    project = Project.query.get(project_id)
    tasks = [
        # ['CheckOut', local_deploy.checkout],
        # ['Static File Minification', local_deploy.change_static_to_pro],
        # ['Database Creation', local_deploy.create_db],
        ['Deployment Setting Change', local_deploy.change_settings],
        ['Apache Vhost Add', local_deploy.create_vhost],
        ['Server Restart', local_deploy.server_restart]
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
        'PRODUCT_TITLE': '\'LinesPay\'',
        'DEBUG': 'False',
        'PRODUCTION': 'True',
        # 'DIVINEMAIL_IP' : '',
        '\'NAME\':': '\'testdb\',',
        '\'USER\':': '\'HUZR\',',
        '\'PASSWORD\':': '\'123\',',
        'BIRTVIEWER_DIR': '\'D:\\\\birt\\\\\'',
        'COMPANY_NAME': '\'HZ\''
    }

    apache_conf_file_path = 'D:\\works\\httpd.conf'

    args_list = [
        # [project.vcs_repo, project.project_dir,'',''],
        # [os.path.join(project.project_dir, 'public', 'static')],
        # [project.mysql_db_name, sql_paths, 'root', '', 'localhost'],
        [project.project_dir, changes_dict],
        [apache_conf_file_path, project.project_dir, str(project.instance_port)],
        []
    ]

    result = []

    for i in range(len(tasks)):
        q = Queue.Queue()
        args_list[i].append(q)
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
        t.join()
        result.append(q.get())
        completed_tasks += 1

        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Completed: {}/{} tasks'.format(str(completed_tasks), str(len(tasks)))
                # 'cmd': result['cmd'],
                # 'output': result['out'].split('\n')
            }
        )
        time.sleep(2)

    self.update_state(state='PROGRESS', meta={'status': 'Finishing Deployment Process.....'})
    time.sleep(4)

    project.is_deployed = 1
    db.session.commit()
    #print result
    #store log file in disk

    return {'status': 'All Tasks Completed!', 'result': 'Project Deployment Completed!', 'log': result}


# ###########################################################################
# Prism ERP deploy procedure
@celery_obj.task(bind=True)
def PrismERPDeploy(self, project_id):
    import threading, time, os, random, Queue
    from fabfile.fabfile import remote_deploy

    project = Project.query.get(project_id)
    tasks = [
        # ['Check Out', remote_deploy.checkout],
        # ['Static File Minification', remote_deploy.change_static_to_pro],
        # ['Database Creation', remote_deploy.create_db],
        # ['Deployment Setting Change', remote_deploy.change_settings],
        # ['Apache Vhost Add', remote_deploy.create_vhost],
        ['Server Restart', remote_deploy.server_restart]
    ]

    completed_tasks = 0

    # Dummy Steps
    self.update_state(state='INITIAL', meta={'status': 'Preparing to deploy......'})
    time.sleep(4)
    self.update_state(state='INITIAL', meta={'status': 'Gathering resources......'})
    time.sleep(4)

    sql_paths = [
        os.path.altsep.join([project.project_dir, 'database', 'prism.sql']),
        os.path.altsep.join([project.project_dir, 'database', 'sphere.sql']),
        os.path.altsep.join([project.project_dir, 'database', 'lines.sql'])
    ]

    changes_dict = {
        'INTERNAL_NAME': '\'prism\'',
        'PRODUCT_NAME': '\'Sphere\'',
        'PRODUCT_TITLE': '\'LinesPay\'',
        'DEBUG': 'False',
        'PRODUCTION': 'True',
        # 'DIVINEMAIL_IP' : '',
        '\'NAME\':': '\'testdb\',',
        '\'USER\':': '\'HUZR\',',
        '\'PASSWORD\':': '\'123\',',
        'BIRTVIEWER_DIR': '\'D:\\\\birt\\\\\'',
        'COMPANY_NAME': '\'HZ\''
    }

    apache_conf_file_path = '/etc/httpd/conf/httpd.conf'
    machine = Machine.query.get(1)

    args_list = [
        # [project.vcs_repo, project.project_dir,'palash','P@@slash'],
        # [os.path.altsep.join([project.project_dir, 'public', 'static'])],
        # [project.mysql_db_name, sql_paths, machine.mysql_username, machine.mysql_password, 'localhost'],
        # [project.project_dir, changes_dict],
        # [apache_conf_file_path, project.project_dir, str(project.instance_port)],
        []
    ]

    result = []

    for i in range(len(tasks)):
        q = Queue.Queue()
        args_list[i].append(q)
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
        t.join()
        result.append(q.get())
        completed_tasks += 1
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Completed: {}/{} tasks'.format(str(completed_tasks), str(len(tasks)))
                # 'cmd': result['cmd'],
                # 'output': result['out'].split('\n')
            }
        )
        time.sleep(2)

    self.update_state(state='PROGRESS', meta={'status': 'Finishing Deployment Process.....'})
    time.sleep(4)

    project.is_deployed = 1
    db.session.commit()
    #print result
    #store log file in disk

    return {'status': 'All Tasks Completed!', 'result': 'Project Deployment Completed!', 'log': result}