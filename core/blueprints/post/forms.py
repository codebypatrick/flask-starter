from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Whats on your mind?', validators=[DataRequired()])

