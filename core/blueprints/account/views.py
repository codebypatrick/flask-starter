from flask import render_template, url_for, redirect, request, flash, abort
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy import or_
from . import account
from .forms import RegisterForm, LoginForm, ProfileForm 
from ...models import User

@account.before_app_request
def before_request():
    """ Refresh last visit (last_seen) """
    if current_user.is_authenticated:
        current_user.ping()
    #check confirmed users only and redirect to confirm page


@account.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(or_(
            User.username == form.email.data,
            User.email == form.email.data
            )).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('home.index'))
        flash('Invalid username or email', 'is-danger')

    return render_template('login.html', form=form)

@account.route('/join', methods=['GET', 'POST'])
def join():
    form = RegisterForm()

    if form.validate_on_submit():
        username=form.username.data
        email=form.email.data
        password=form.password.data
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        user.save()

        flash('You can now login', 'is-info')
        return redirect(url_for('account.login'))

    return render_template('join.html', form=form)

@account.route('/reset-password')
def reset_password():
    return 'reset password'

@account.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out', 'is-warning')
    return redirect(url_for('account.login'))


@account.route('/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):

    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)

    form = ProfileForm()
    if form.validate_on_submit():
        user.about_me = form.about_me.data
        user.save()
        flash('Your profile was updated', 'is-info')

    form.about_me.data = user.about_me

    return render_template('profile.html', user=user, form=form)
