from .extentions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from markdown import markdown
import bleach
from slugify import slugify

# Define base model for other tables to inherit
class Base(db.Model):
    __abstract__ = True

    # number of items per page in pagination
    PER_PAGE = 10

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(), default= datetime.now)
    modified = db.Column(db.DateTime(), default=datetime.now)


    # Save given instance of model
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Delete given instance of model
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(UserMixin, Base):

    __tablename__ = 'users'

    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.now)
    last_seen = db.Column(db.DateTime(), default=datetime.now)
    last_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(25))
    current_login_at = db.Column(db.DateTime)
    current_login_ip = db.Column(db.String(25))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def ping(self):
        """ Refresh last visit (last_seen) of user """
        self.last_seen = datetime.now()
        db.session.add(self)
        db.session.commit()


# load user in login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Many to Many tags to posts
tags = db.Table('post_tags',
        db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
        db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
        )

class Post(Base):
    __tablename__ = 'posts'

    title = db.Column(db.String(255))
    body = db.Column(db.Text())
    slug = db.Column(db.String(255))
    body_html = db.Column(db.Text())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    tags = db.relationship('Tag',
            secondary=tags,
            backref=db.backref('posts', lazy='dynamic'),
            lazy='dynamic'
            )

    #def __init__(self, title, body):
        #self.title = title
        #self.body = bod

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'p', 'h1', 'h2', 'h3', 'code', 'em',
                'strong', 'pre', 'ul']
        # add more allowed tags

        target.body_html = bleach.linkify(
                bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True)
                )


#Event listeners on post model
db.event.listen(Post.body, 'set', Post.on_changed_body)
db.event.listen(Post.title, 'set', Post.generate_slug, retval=False)


class Comment(Base):

    __tablename__ = 'comments'

    body = db.Column(db.Text())
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

class Tag(Base):
    __tablename__ = 'tags'

    title = db.Column(db.String(), unique=True, nullable=True)
