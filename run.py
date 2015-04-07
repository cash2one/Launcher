__author__ = 'HZ'


from Launcher import app

import netifaces as ni
#for nt
ip = ni.ifaddresses(ni.gateways()[2][0][1])[2][0]['addr']

try:
    app.run(host=ip, port=5000, debug=app.debug)
except:
    app.run(host='127.0.0.1', port=5000, debug=app.debug)
