from flask import render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import or_
from . import auth
from .forms import LoginForm,  RegisterForm, ChangePasswordForm, ForgotPasswordForm, PasswordResetRequestForm
from .. import db
from ..models import User
from ..util import send_mail

@auth.route('/join', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
                )
        db.session.add(user)
        db.session.commit()

        subject = 'Confirm your email'
        token = user.generate_confirm_token()
        confirm_url = url_for('.confirm_email', token=token, _external=True)

        html = render_template('auth/activate.html', confirm_url=confirm_url)
        send_mail(user.email, subject, html)
        flash('A confiration link has been sent to your email address.', 'is-info')
        return redirect(url_for('main.index'))
    return render_template('auth/join.html', form=form, title='Register')

@auth.route('/confirm/<token>')
@login_required
def confirm_email(token):
    if current_user.confirmed:
        flash('Your account is already confirmed', 'is-warning')
        return redirect(url_for('main.index'))
    if current_user.verify_confirm_token(token):
        flash('Your account is confirmed!', 'is-info')
    else:
        flash('The confirmation link is invalid or expired')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    subject = 'Confirm Your Account'
    token = current_user.generate_confirm_token()
    confirm_url = url_for('.confirm_email', token=token, _external=True)
    send_mail(user.email, subject, html)
    flash('A new confirmation link has been sent to your email', 'is-info')
    return redirect(url_for('main.index'))

@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html', title='Unconfirmed')

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated!', 'is-info')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password')

    return render_template('auth/change_password.html', form=form, title='Change Password')

@auth.route('/reset')
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = user.query.filter_by(email=form.email.data).first_or_404()

        subject = 'Password Reset Requested'
        token = user.generate_reset_token(form.email.data)
        reset_url = url_for('.reset_with_token', token=token, _external=True)
        html = render_template(
                'auth/password_reset.html',
                reset_url=reset_url)
        send_mail(form.email.data, subject, html)
        flash('An email with instructions to reset your password has been sent to you.', 'is-info')

    return render_template('auth/forgot_password.html', form=form, title='Forgot Password')

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.verify_reset_token(form.password.data):
            flash('Your password was updated', 'is-info')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form, title='Reset Password')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(
                or_(
                    User.username == form.email_username.data,
                    User.email == form.email_username.data)
                ).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invaild Credienials or Password', 'danger')

    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
def logout():
    logout_user()
    flash('You are logged out')
    return redirect(url_for('main.index'))

