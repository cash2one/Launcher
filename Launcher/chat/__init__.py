from flask import Blueprint

chat = Blueprint('chat', __name__)

import routes, events