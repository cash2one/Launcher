__author__ = 'HZ'

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