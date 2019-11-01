from flask import render_template
from flask_login import current_user, login_required
from . import main

@main.route('/')
def index():
    return render_template('main/index.html', title='Home')

@main.route('/me')
@login_required
def profile():
    return 'Profile'
