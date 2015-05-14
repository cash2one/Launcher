"""
Module: tasklist.py
Author: HZ
-------------------
Contains the list of tasks.
"""

from fabric.api import abort, cd, env, get, hide, hosts, local, prompt, put, require, roles, run, runs_once, settings, \
    show, sudo, warn

from taskset import TaskSet, task_method


# Deployment Task Class: Full Deployment of a new project
class PrismDeployment(TaskSet):
    """Deployment of a new project"""

    def run_task(self, cmd):
        """Runs the task as given in the command"""
        # Not initialized here...must be overloaded from outside
        raise NotImplementedError()

    @task_method
    def checkout(self, svn_repo, co_dir, svn_username='', svn_password='', queue=None):
        """Initial checkout from SVN repository; must provide repo and co dir at least; credentials are optional"""
        if not svn_username and not svn_password:
            try:
                cmd = ' '.join(['svn co', svn_repo, co_dir])
            except Exception as e:
                raise Exception(e)
        elif (svn_username and not svn_password) or (not svn_username and svn_password):
            raise Exception("Must provide both SVN username and password")
        else:
            try:
                cmd = ' '.join(['svn', 'co', '--username', svn_username, '--password', svn_password, '--no-auth-cache', svn_repo, co_dir])
            except Exception as e:
                raise Exception(e)

        out = self.run_task(cmd)

        if queue:
            cmd = 'svn co {} {}'.format(svn_repo, co_dir)
            queue.put([cmd, out.split('\n')])


    @task_method
    def change_static_to_pro(self, path_to_static, queue=None):
        """Converts the Static contents and makes production ready"""
        import os

        compressor = os.path.altsep.join([path_to_static, 'compressor.py'])
        media = os.path.altsep.join([path_to_static, 'media.py'])

        if self.SHELL == 'Local':
            pass
        elif self.SHELL == 'Remote':
            #delete old compressor and media py files with os independent corrections
            self.run_task('rm -f {}'.format(compressor))
            new = os.path.join(os.path.dirname(__name__), 'tmp', 'compressor.py')
            put(new, path_to_static)

            #new = os.path.join(os.path.dirname(__name__), 'tmp', 'media.py')
            #self.run_task('rm -f {}'.format(media))
            get(media, os.path.join(os.path.dirname(__name__), 'tmp'))
            new = os.path.join(os.path.dirname(__name__), 'tmp', 'media.py')
            temp = os.path.join(os.path.dirname(__name__), 'tmp', 'media_temp.py')

            n = open(new, 'r')
            t = open(temp, 'w')

            for each in n.readlines():
                if 'jdmenu' in each:
                    t.write(each.replace('jdmenu', 'jdMenu'))
                else:
                    t.write(each)
            n.close()
            t.close()

            os.remove(n.name)
            os.rename(t.name, n.name)

            self.run_task('rm -f {}'.format(media))
            put(new, path_to_static)
            os.remove(new)

        #needs the dir context eg. #local('cd /D E:\\Prism\\divineba\\public\\static && dir')
        #that was the problem of the old compressor script....redone by HZ to avoid that...
        cmd = ' '.join(['python', compressor])
        out = self.run_task(cmd)

        if queue:
            queue.put([cmd, out.split('\n')])


    @task_method
    def create_db(self, db_name, sql_paths_list=[], db_user='root', db_pass='', db_host='localhost', queue=None):
        """Creates the db and runs sql"""

        path = ''
        #makes the list when obtained from command line, backend can pass list directly
        if isinstance(sql_paths_list, str):
            sql_paths_list = sql_paths_list.split(';')

        if db_pass:
            cmd = path + 'mysql -u{0} -h{1} -p{2} -e "create database {3};"'.format(db_user, db_host, db_pass, db_name)
        else:
            cmd = path + 'mysql -u{0} -h{1} -e "create database {2};"'.format(db_user, db_host, db_name)

        to_put = []
        out = self.run_task(cmd)
        cmd = 'mysql create database {}'.format(db_name)
        to_put.append([cmd, out.split('\n')])

        for each in sql_paths_list:
            if db_pass:
                cmd = path + 'mysql -u{0} -h{1} -p{2} {3} < '.format(db_user, db_host, db_pass, db_name) + each
            else:
                cmd = path + 'mysql -u{0} -h{1} {2} < '.format(db_user, db_host, db_name) + each

            out = self.run_task(cmd)
            cmd = 'mysql execute sql {}'.format(each)
            to_put.append([cmd, out.split('\n')])

        if queue:
            queue.put(to_put)


    @task_method
    def change_settings(self, project_dir, changes_dict, queue=None):
        """Change variable values of settings_deploy as per client"""

        import os

        #ToDo: Changes Dict must be parsed in case of cmd input, sep as ;
        if isinstance(changes_dict, str):
            changes_dict = {
                #'INTERNAL_NAME':'\'PRISM\'',
                #'PRODUCT_NAME': '\'Sphere\'',
                #'COMPANY_NAME': '\'HZ\''
            }

        if self.SHELL == 'Remote':
            #gets the settings_deploy file from remote host, and puts it in tmp/ directory of fabfile dir
            remote_settings_deploy = project_dir + '/' + 'settings_deploy.py'

            get(remote_settings_deploy, 'tmp')
            settings_deploy = os.path.join(os.path.dirname(__name__),'tmp','settings_deploy.py')
            settings_to_deploy = os.path.join(os.path.dirname(__name__), 'tmp', 'settings_to_deploy.py')

        elif self.SHELL == 'Local':
            #creates a temp file in the project directory, makes the new settings file and deletes the original file, renames the temp
            settings_deploy = os.path.join(project_dir, 'settings_deploy.py')
            settings_to_deploy = os.path.join(project_dir, 'setting_to_deploy.py')
        else:
            raise Exception('Shell type was not given properly!')

        try:
            #change process occurs in local machine
            if os.path.exists(settings_deploy):
                sd = open(settings_deploy, 'r')
                settings_to_deploy = open(settings_to_deploy, 'w')
                settings_to_change = ['INTERNAL_NAME', 'PRODUCT_NAME', 'PRODUCT_TITLE', 'DEBUG', 'PRODUCTION',
                                      'DIVINEMAIL_IP',
                                      '\'NAME\':', '\'USER\':', '\'PASSWORD\':', 'BIRTVIEWER_DIR',
                                      'BIRTVIEWER_PORT', 'COMPANY_NAME', 'EMAIL_API_URL', 'EMAIL_API_USER',
                                      'EMAIL_API_PASSWORD', 'EMAIL_API_CALLBACK_URL']

                change = True

                for each in sd.readlines():
                    if each.startswith('try'):
                        change = False
                    try:
                        if each.split()[0] in settings_to_change and change:
                            if each.split()[0] == 'COMPANY_NAME':
                                settings_to_deploy.write(
                                    each.replace(each.split(' = ')[-1], changes_dict[each.split()[0]]) + '\n')
                            else:
                                settings_to_deploy.write(each.replace(each.split()[-1], changes_dict[each.split()[0]]))
                        else:
                            settings_to_deploy.write(each)
                    except:
                        settings_to_deploy.write(each)

                sd.close()
                settings_to_deploy.close()
                os.remove(sd.name)
                os.rename(settings_to_deploy.name, sd.name)

            else:
                raise Exception('Settings Deploy Not Found!')


        except Exception as e:
            raise Exception(e)

        if self.SHELL == 'Remote':
            with cd(project_dir):
                cmd = 'rm -f ' + remote_settings_deploy
                self.run_task(cmd)
                put(settings_deploy, project_dir, mode=0755)
                os.remove(settings_deploy)

        cmd = 'change settings_deploy.py'
        out = 'Settings Changed Successfully!'
        res = [cmd, out.split('\n')]
        if queue:
            queue.put(res)


    @task_method
    def create_vhost(self, apache_conf_file_path, project_dir, project_port, queue=None):
        """Create the vhost conf and put it in apache conf folder"""
        #append to the one n only httpd.conf....use apacheconfparser before to know the settings?
        import os
        #Apache conf file
        if self.SHELL == 'Local':
            if os.path.exists(apache_conf_file_path):
                httpd = apache_conf_file_path
            else:
                raise Exception('Apache Config file httpd.conf not found!')
        elif self.SHELL == 'Remote':
            get(apache_conf_file_path, 'tmp')
            httpd = os.path.join(os.path.dirname(__name__), 'tmp', 'httpd.conf')
        else:
            raise Exception('Shell type was not given properly!')

        #parse apache conf info here?
        import ApacheParser as AP
        from ApacheSections import parse_section

        #create config object and parse the file
        c = AP.ApacheConfig('httpd')
        confs = c.parse_file(httpd)
        configs = parse_section(confs.children)

        ports = [each[1][0] for each in configs if each[0]=='Listen']
        unneeded = [each[0] for each in configs if each[0] in ('WSGIPythonPath', 'WSGIRestrictStdin', 'WSGIRestrictStdout')]

        print apache_conf_file_path, project_dir, project_port
        #create the vhost conf
        try:
            project_dir = project_dir.rstrip('/')
            project_dir = project_dir.rstrip('\\')

            if ('/' in project_dir and '/' != os.path.sep) or ('\\' in project_dir and '\\' != os.path.sep):
                os.path.sep = os.path.altsep

            PATH_TO_PROJECT_ROOT = project_dir
            PORT = project_port
            PATH_TO_PUBLIC_DIR = os.path.sep.join([project_dir, 'public'])
            PATH_TO_STATIC = os.path.sep.join([PATH_TO_PUBLIC_DIR, 'static'])
            PATH_TO_DIVINEBA_WSGI = os.path.sep.join([PATH_TO_PUBLIC_DIR, 'divineba.wsgi'])

            #The PrismERP FurinaPy vhost config template
            vhost = os.path.join(os.path.dirname(__name__), 'tmp', 'PyPrismVhost.conf')
            v = open(vhost, 'r')
            temp = os.path.join(os.path.dirname(__name__), 'tmp', 'new.conf')
            n = open(temp, 'w')

            for each in v.readlines():
                if '{PATH_TO_PROJECT_ROOT}' in each:
                    n.write(each.replace('{PATH_TO_PROJECT_ROOT}', PATH_TO_PROJECT_ROOT))
                elif '{PORT}' in each:
                    if PORT in ports and 'Listen' in each:
                        n.write('#Port already open...')
                        n.write('\n')
                        # n.write(each.replace('{PORT}', PORT))
                    else:
                        n.write(each.replace('{PORT}', PORT))
                elif '{PATH_TO_STATIC}' in each:
                    n.write(each.replace('{PATH_TO_STATIC}', PATH_TO_STATIC))
                elif '{PATH_TO_DIVINEBA_WSGI}' in each:
                    n.write(each.replace('{PATH_TO_DIVINEBA_WSGI}', PATH_TO_DIVINEBA_WSGI))
                elif '{PATH_TO_PUBLIC_DIR}' in each:
                    n.write(each.replace('{PATH_TO_PUBLIC_DIR}', PATH_TO_PUBLIC_DIR))
                else:
                    try:
                        if each.split()[0] in unneeded:
                            continue
                        else:
                            n.write(each)
                    except:
                        n.write(each)

            v.close()
            n.close()

            #append at end of the httpd.conf....local = original....remote = delete original and put

            conf = open(httpd, 'a')
            n = open(temp, 'r')
            conf.write('\n\n')
            for each in n.readlines():
                conf.write(each)

            n.close()
            conf.close()

            if self.SHELL == 'Remote':
                cmd = 'rm -f ' + apache_conf_file_path
                self.run_task(cmd)
                put(httpd, apache_conf_file_path, mode=0755)
                os.remove(httpd)

            os.remove(temp)

        except Exception as e:
            print str(e)
            raise Exception(e)

        cmd = 'create virtualhost'
        out = 'Config Created Successfully!'
        res = [cmd, out.split('\n')]
        if queue:
            queue.put(res)


    @task_method
    def server_restart(self, queue=None):
        """Restart the Apache server...todo: touch the wsgi only without full restart"""
        cmd = 'apachectl graceful'
        out = self.run_task(cmd)
        if queue:
            queue.put([cmd, out.split('\n')])


    @task_method
    def deploy_project(self, svn_repo, co_dir, path_to_static, database_name, apache_conf_file_path, project_port, svn_username='', svn_password='', db_username='', db_password='', sql_paths_list=[], changes_dict={}):
        """Performs all the tasks to deploy a project completely"""
        self.checkout(svn_repo, co_dir, svn_username, svn_password)
        self.change_static_to_pro(path_to_static)
        self.create_db(database_name, sql_paths_list, db_username, db_password)
        self.change_settings(co_dir, changes_dict)
        self.create_vhost(apache_conf_file_path, project_dir=co_dir, project_port=project_port)
        self.server_restart()


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
        self.run_task('apachectl graceful')

    @task_method
    def maintain_project(self, co_dir):
        self.update(co_dir)
        self.run_new_sql()
        self.server_restart()


class LocalShell(object):
    """Performs commands in local shell"""

    SHELL = 'Local'

    def run_task(self, cmd):

        with settings(warn_only=True):
            out = local(cmd, True)
            if out.return_code == 0:
                # use this to catch msg and halt task executions
                print "Success"
            else:
                print "FAILED!!"
                out = 'FAILED'

            return out


class RemoteShell(object):
    """Performs commands in a remote shell"""

    SHELL = 'Remote'

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
            out = run(cmd, True)
            if out.return_code == 0:
                #use this to catch msg and halt task executions
                print "Success"
            else:
                print "FAILED!!"
                out = 'FAILED'

            return out


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