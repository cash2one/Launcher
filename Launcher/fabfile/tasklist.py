"""
Module: tasklist.py
Author: HZ
-------------------
Contains the list of tasks.
"""

from fabric.api import abort, cd, env, get, hide, hosts, local, prompt, put, require, roles, run, runs_once, settings, \
    show, sudo, warn

from taskset import TaskSet, task_method

#import fabtools

# Deployment Task Class: Full Deployment of a new project
class PrismDeployment(TaskSet):
    """Deployment of a new project"""

    def run_task(self, cmd):
        """Runs the task as given in the command"""
        # Not initialized here...must be overloaded from outside
        raise NotImplementedError()

    @task_method
    def checkout(self, svn_repo, co_dir, svn_username='', svn_password=''):
        """Initial checkout from SVN repository; must provide repo and co dir at least; credentials are optional"""
        if not svn_username and not svn_password:
            try:
                self.run_task(' '.join(['svn co', svn_repo, co_dir]))
            except Exception as e:
                raise Exception(e)
        elif (svn_username and not svn_password) or (not svn_username and svn_password):
            raise Exception("Must provide both SVN username and password")
        else:
            try:
                self.run_task(' '.join(['svn', 'co', '--username', svn_username, '--password', svn_password, '--no-auth-cache', svn_repo, co_dir]))
            except Exception as e:
                raise Exception(e)

    @task_method
    def change_static_to_pro(self, path_to_static):
        """Converts the Static contents and makes production ready"""

        #needs the dir context eg. #local('cd /D E:\\Prism\\divineba\\public\\static && dir')
        self.run_task(' '.join(['cd', path_to_static, '&&', 'python', 'compressor.py']))

    @task_method
    def create_db(self, db_name, sql_paths_list=[], db_user='root', db_pass='', db_host='localhost'):
        """Creates the db and runs sql"""

        #path = "c:\\wamp\\bin\\mysql\\mysql5.0.51b\\bin\\"
        #path not needed if mysql installed as server
        path = ''
        #makes the list when obtained from command line, backend can pass list directly
        if isinstance(sql_paths_list, str):
            sql_paths_list = sql_paths_list.split(';')

        #self.run_task(path+'mysql -uroot -hlocalhost -e "show databases;"')
        #self.run_task(path+'mysql -uroot -hlocalhost -e "drop database testdb;drop database testdb1;"')
        #self.run_task(path+'mysql -uroot -hlocalhost -e "show tables in testdb;"')
        if db_pass:
           self.run_task(path + 'mysql -u{0} -h{1} -p{2} -e "create database {3};"'.format(db_user, db_host, db_pass, db_name))
        else:
            self.run_task(path + 'mysql -u{0} -h{1} -e "create database {2};"'.format(db_user, db_host, db_name))

        #sql paths from cod project's path
        #put("D:\#HZ\ex1.sql",'/var/www/')

        for each in sql_paths_list:
            if db_pass:
                self.run_task(path + 'mysql -u{0} -h{1} -p{2} {3} < '.format(db_user, db_host, db_pass, db_name) + each)
            else:
                self.run_task(path + 'mysql -u{0} -h{1} {2} < '.format(db_user, db_host, db_name) + each)

        # if db_pass:
        #     self.run_task(
        #         path + 'mysql -u{0} -h{1} -p{2} -e "drop database {3};"'.format(db_user, db_host, db_pass, db_name))
        # else:
        #     self.run_task(path + 'mysql -u{0} -h{1} -e "drop database {2};"'.format(db_user, db_host, db_name))

        #self.run_task(path + 'mysql -uroot -hlocalhost testdb < '+ "E:\Prism4\Prism4\divineba\database\prism.sql")
        #self.run_task('mysql -u root -pR#2a87Gsre@1 -e "show databases;"')
        # create database, run sql on that db
        #self.run_task('mysql -pR#2a87Gsre@1 -e "CREATE DATABASE testdb;"')
        #self.run_task('mysql -pR#2a87Gsre@1 -e "show databases;"')
        #self.run_task('mysql -pR#2a87Gsre@1 -e "DROP DATABASE testdb;"')
        #self.run_task('mysql -pR#2a87Gsre@1 -e "show databases;"')

    def change_settings(self):
        """Change variable values of settings_deploy as per client"""
        pass

    def create_vhost(self):
        """Create the vhost conf file and put it in apache conf folder"""
        vhost = '''#Project wsgi app config
        WSGIPythonPath / /usr/local/lib/python2.7
        WSGIRestrictStdin Off
        WSGIRestrictStdout Off

        <VirtualHost *:80>
        	Alias /static /var/www/divineba/public/static
                WSGIScriptAlias / /var/www/divineba/public/divineba.wsgi
                <Directory /var/www/divineba/public>
        		Order deny,allow
        		Allow from all
                        AddOutputFilterByType DEFLATE text/css text/javascript application/javascript text/html text/plain text/xml
                </Directory>
        </VirtualHost>
        '''
        pass

    @task_method
    def server_restart(self):
        """Restart the Apache server...todo: touch the wsgi only without full restart"""
        self.run_task('service httpd restart')

    @task_method
    def deploy_project(self, svn_repo, co_dir, path_to_static, database_name, svn_username='', svn_password='', db_username='', db_password='', sql_paths_list=[]):
        """Performs all the tasks to deploy a project completely"""
        self.checkout(svn_repo, co_dir, svn_username, svn_password)
        self.change_static_to_pro(path_to_static)
        self.create_db(database_name, db_username, db_password, sql_paths_list)
        # self.change_settings()
        # self.create_vhost()
        # self.server_restart()


# Maintenance Task Class: Maintenance of an existing project
class PrismMaintenance(TaskSet):
    """Maintenance of a project"""

    def run_task(self, cmd):
        """Runs the task as given in the command"""
        # Not initialized here...must be overloaded from outside
        raise NotImplementedError()

    def update(self, co_dir):
        """SVN update of already checked out repo"""
        self.run_task(' '.join(['svn', 'up', co_dir]))
        pass

    def run_new_sql(self):
        """Get the diffs of sqls, use the output dumped on a file to make a temp sql, then run it on mysql"""

        pass

    @task_method
    def server_restart(self):
        """Restart the Apache server...todo: touch the wsgi only without full restart"""
        self.run_task('service httpd restart')

    @task_method
    def maintain_project(self, co_dir):
        self.update(co_dir)
        self.run_new_sql()
        self.server_restart()


class LocalShell(object):
    """Performs commands in local shell"""

    def run_task(self, cmd):
        with settings(warn_only=True):
            res = local(cmd, True)
            if res.return_code == 0:
                # use this to catch msg and halt task executions
                print "Success"
            else:
                print "FAILED!!"
            return res


class RemoteShell(object):
    """Performs commands in a remote shell"""

    def __init__(self, environment={}):
        # env.user = environment['user']
        # env.hosts = environment['hosts']
        # env.port = environment['port']
        # env.passwords = environment['passwords']
        try:
            env.host_string = environment['user'] + '@' + environment['hosts'][0] + ':' + str(environment['port'])
            env.password = environment['passwords'][env.host_string]
        except:
            print 'No environment given, will prompt in Shell'

    def run_task(self, cmd):
        with settings(warn_only=True):
            res = run(cmd, True)
            if res.return_code == 0:
                #use this to catch msg and halt task executions
                print "Success"
            else:
                print "FAILED!!"
            return res


# LocalDeployment Class: Applicable for local deployment
class LocalDeployment(LocalShell, PrismDeployment):
    """Deploys in a local machine"""
    pass


# RemoteDeployment Class: Applicable for remote deployment
class RemoteDeployment(RemoteShell, PrismDeployment):
    """Deploys in a remote machine"""
    pass


# LocalMaintenance Class: Applicable for local maintenance
class LocalMaintenance(LocalShell, PrismMaintenance):
    """Maintains project present in a local machine"""
    pass


# RemoteMaintenance Class: Applicable for remote maintenance
class RemoteMaintenance(RemoteShell, PrismMaintenance):
    """Maintains project present in a local machine"""
    pass