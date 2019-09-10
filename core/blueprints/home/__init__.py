from flask import Blueprint

home = Blueprint('home', __name__, url_prefix='/')

from . import views
