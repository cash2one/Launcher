"""
Module: commands.py
Author: HZ

This module contains custom made actions for running through the management script of the application.
"""

from flask_script import Command, Option
from fabric.api import local


class Celery_Script(Command):
    """Custom script for initiating celery service"""

    def __init__(self, app_name='Launcher.celery_obj', log_file='logs\\celery.worker.log', loglevel='INFO'):
        self.app_name = app_name
        self.log_file = log_file
        self.loglevel = loglevel

    def get_options(self):
        return [
            Option('-A', '--capp', dest='capp', default=self.app_name, required=False),
            Option('-f', '--logfile', dest='logfile', default=self.log_file, required=False),
            Option('-l', '--loglevel', dest='loglevel', default=self.loglevel, required=False)
        ]

    def run(self, capp, logfile, loglevel):
        local('celery worker -A {0} -f {1} --loglevel={2}'.format(capp, logfile, loglevel))


class Flower_Script(Command):
    """Custom script for initiating flower server"""

    def run(self):
        local('celery flower --broker=redis://localhost:6379/0 --persistent=True --db=logs\\flower.db')