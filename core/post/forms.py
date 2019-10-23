from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Content', validators=[DataRequired()])

class CommentForm(Form):
    body = TextAreaField('Comment', validators=[DataRequired()])
