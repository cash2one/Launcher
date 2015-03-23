"""
Module: credentials.py
Author: HZ

Access credentials for a remote server.
"""

USER = 'root'
HOSTS = ['qa.divineit.net']
PORT = 44145
PASSWORDS = {
    USER+'@'+HOSTS[0]+':'+str(PORT): 'Szyy400Div'
}

