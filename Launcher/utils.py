"""
Module: utils.py
Author: HZ
Created: March 25, 2015

Description: 'Custom Utils for the project'
"""

import base64
from datetime import timedelta

DST = timedelta(hours=6)


def pwd_encryption(password):
    for i in range(3):
        password = base64.b64encode(password)
    return password


def pwd_decryption(password):
    for i in range(3):
        password = base64.b64decode(password)
    return password


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
