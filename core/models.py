from . import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from markdown import markdown
import bleach

class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default = db.func.current_timestamp())
    modified = db.Column(db.DateTime, default = db.func.current_timestamp(), onupdate = db.func.current_timestamp())

class User(Base, UserMixin):
    __tablename__ = 'users'

    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String())
    about_me = db.Column(db.Text)
    confirmed = db.Column(db.Boolean, default=False) 
    roles = db.relationship('Role', secondary='user_roles')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.set_password(self.password)


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_confirm_token(self, max_age=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=max_age)
        return s.dumps({'confirm': self.id})

    def verify_confirm_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        
        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def generate_reset_token(self, max_age=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'reset': self.id})

    def verify_reset_token(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('reset') != self.id:
            return False

        self.set_password(new_password)
        db.session.add(self)
        db.session.commit()
        return True

    def add_role(self, role_id):
        role = Role.query.get(role_id)
        self.roles.append(role)

    def remove_role(self, role_id):
        role = Role.query.get(role_id)
        self.roles.remove(role)

    def has_role(self, *requirements):
        for requirement in requirements:
            for role in requirement:
                for r in self.roles:
                    if r.name == role:
                        return True 
        return False

    def is_administrator(self):
        for role in self.roles:
            if role.name == 'Admin':
                return True
        return False
    
    def __repr__(self):
        return '<User: %r>' % self.username 

class AnonymousUser(AnonymousUserMixin):
    def has_role(self, requirements):
        return False

    def is_administrator(self):
        return False
    

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(Base):
    __tablename__ = 'roles'

    name = db.Column(db.String(64), unique=True)

    @staticmethod
    def insert_roles():
        roles = ['Admin', 'Poster', 'Moderator']
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            db.session.add(role)
            
        db.session.commit()
    def __repr__(self):
        return '<Role: %r>' % self.name

class UserRoles(db.Model):
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))

class Post(Base):
    __tablename__ = 'posts'

    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['h2', '<p>', 'a', 'ul', 'li', 'ol', 'b', 'strong']


        target.body_html = bleach.linkify(
                bleach.clean(
                    markdown(value, output_format='html'), allowed_tags, strip=True)
                )

    def __repr__(self):
        return '<Post: %r>' % self.title

db.event.listen(Post.body, 'set' , Post.on_changed_body)

class Comment(Base):
    __tablename__ = 'comments'

    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'p', 'strong']

        target.body_html = bleach.linkify(
                bleach.clean( markdown(value, output_format='html'), allowed_tags, strip=True )
                )

db.event.listen(Post.body, 'set', Post.on_changed_body)
