"""
Module: shells.py
Author: HZ
-----------------
This module holds the Shell Object Type.
Fabric commands runs on local or remote machine depending on its type.
"""


class FabulouSSH(object):
    """Creates an SSH object...can be either Local or Remote"""
    
    def __init__(self, type):
        """Initializes the Shell object type"""
        if str(type).lower() not in ['local', 'remote']:
            raise Exception('Provide valid "type" as "local" or "remote" to create proper SSH')
        else:
            self.TYPE = type.lower()