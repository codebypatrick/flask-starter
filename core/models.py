from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String())
    confirmed = db.Column(db.Boolean, default=False) 

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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

