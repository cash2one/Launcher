#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module: run_app.py
Author: HZ
Created: Mar 23, 2015

Description: 'Shortcut python script for running the app...can also be done from management.'
"""

# global imports below: built-in, 3rd party, own
import netifaces as ni
from Launcher import app, socketio
from gevent import monkey


# Ownership information
__author__ = 'HZ'
__copyright__ = "Copyright 2015, HZ, Divine IT Ltd."
__credits__ = ["HZ"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "HZ"
__email__ = "hz.ce06@gmail.com"
__status__ = "Development"


def run_application():
    # for nt, mayb for unix too
    monkey.patch_all()
    #TODO: can take cmd arguments for host, port, debug
    ip = ni.ifaddresses(ni.gateways()[2][0][1])[2][0]['addr']
    try:
        #app.run(host=ip, port=5000, debug=app.debug)
        socketio.run(app, host=ip, port=5000)
    except:
        #app.run(host='127.0.0.1', port=5000, debug=app.debug)
        socketio.run(app, host='127.0.0.1', port=5000)


if __name__ == '__main__':
    run_application()