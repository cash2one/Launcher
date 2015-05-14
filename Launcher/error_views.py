__author__ = 'HZ'

from views import *


############################################################################
@app.route('/preview')
@login_required
def test():
    """Dummy route for testing site layout for dev purpose"""

    return render_template('base.html')


# ###########################################################################
# Flask-Security Unauthorized View endpoint
@app.route('/page_not_serveable')
def access_denied():
    """Custom Access Forbidden view"""
    return render_template('errors/403.html')


#########################-----Flask Error views-----#########################
# ###########################################################################
@app.errorhandler(403)
def page_not_serveable(e):
    """Custom Access Forbidden view"""
    return render_template('errors/403.html'), 403


# ###########################################################################
@app.errorhandler(404)
def page_not_found(e):
    """Custom Forbidden view"""
    return render_template('errors/404.html'), 404


# ###########################################################################
@app.errorhandler(405)
def method_not_allowed(e):
    """Custom Method not allowed view"""
    return render_template('errors/405.html'), 405


# ###########################################################################
@app.errorhandler(500)
def server_error(e):
    """Custom internal server error view"""
    return render_template('errors/500.html'), 500
