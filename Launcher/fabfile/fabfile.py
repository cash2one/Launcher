"""
Module: fabfile.py
Author: HZ
-------------------
API for the python Fabric library.
Use from CLI eg.> fab <cmd>.
Use in the backend of applications.
"""

from tasklist import *

# example credential dictionary; must populate during ssh execution or api use
# keep blank for security purposes
info = {}

import credentials

info = {
    'user': credentials.USER,
    'hosts': credentials.HOSTS,
    'port': credentials.PORT,
    'passwords': credentials.PASSWORDS,
}



# creating the tasks
#Project Deployment
local_deploy = LocalDeployment().expose_as_module('local_deploy')
remote_deploy = RemoteDeployment(info).expose_as_module('remote_deoploy')
#Project Maintenance
local_maintain = LocalMaintenance().expose_as_module('local_maintain')
remote_maintain = RemoteMaintenance(info).expose_as_module('remote_maintain')
