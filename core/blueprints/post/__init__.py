from flask import Blueprint

post = Blueprint('post', __name__, url_prefix='/posts', template_folder='templates')

from . import views
