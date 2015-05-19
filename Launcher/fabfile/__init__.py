#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module: fabfile
Author: HZ
Created: March 01, 2015

Description: 'This package holds the fabric tasks defined for the launcher project. This also acts as an API.'
Usage:
    >>> fab -l
    Output shows the list of available fabric tasks.
    >>> fab tasks.remote_deploy.deploy_project: <all the parameters here...must know what you are doing>
    Watch the full project auto deployed if all goes well
"""

# global imports below: built-in, 3rd party, own
import fabfile as tasks


# Ownership information
__author__ = 'HZ'
__copyright__ = "Copyright 2015, HZ, Divine IT Ltd."
__credits__ = ["HZ"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "HZ"
__email__ = "hz.ce06@gmail.com"
__status__ = "Development"

