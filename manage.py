#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module: manage.py
Author: HZ
Created: Apr 8, 2015

Description: 'This module bears custom made management commands which can be run for the application context.'
"""

# global imports below: built-in, 3rd party, own
from flask.ext.script import Manager
from flask.ext.script.commands import Server, Shell, ShowUrls, Clean
from flask.ext.security.script import CreateUserCommand, AddRoleCommand, RemoveRoleCommand, ActivateUserCommand, DeactivateUserCommand

from Launcher import app
#from flask_application.script import ResetDB, PopulateDB
#from flask_application.tests.script import RunTests
from management import Celery_Script, Flower_Script
from run_app import run_application

# Ownership information
__author__ = 'HZ'
__copyright__ = "Copyright 2015, HZ, Divine IT Ltd."
__credits__ = ["HZ"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "HZ"
__email__ = "hz.ce06@gmail.com"
__status__ = "Development"


manager = Manager(app)
manager.add_command("shell", Shell(use_ipython=True))
# manager.add_command("runserver", Server(use_reloader=True))
manager.add_command("runserver", run_application())
manager.add_command("show_urls", ShowUrls())
manager.add_command("clean", Clean())

#manager.add_command("reset_db", ResetDB())
#manager.add_command("populate_db", PopulateDB())

manager.add_command('create_user', CreateUserCommand())
manager.add_command('add_role', AddRoleCommand())
manager.add_command('remove_role', RemoveRoleCommand())
manager.add_command('deactivate_user', DeactivateUserCommand())
manager.add_command('activate_user', ActivateUserCommand())

#manager.add_command('run_tests', RunTests())

manager.add_command('celery', Celery_Script())
manager.add_command('flower', Flower_Script())


if __name__ == "__main__":
    manager.run()
