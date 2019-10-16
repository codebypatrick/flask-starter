from functools import wraps
from flask_login import current_user
from flask import abort, url_for, redirect, flash

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.has_role(role):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def confirmed_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('auth.unconfirmed'))
        return f(*args, **kwargs)
    return decorated_function
