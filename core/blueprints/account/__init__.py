from flask import Blueprint

account = Blueprint('account', __name__, url_prefix='/account', template_folder='templates')

from . import views
