from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from ..models import User

class RegisterForm(Form):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already taken')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

class ChangePasswordForm(Form):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])

class ForgotPasswordForm(Form):
    email = StringField('Email Address', validators=[DataRequired(), Email()])

class PasswordResetRequestForm(Form):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])

class LoginForm(Form):
    email_username = StringField('Email or Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')

class ProfileForm(Form):
    about_me = TextAreaField('About Me')

