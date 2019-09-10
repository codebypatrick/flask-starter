from flask import Flask

from .config import config
from .extentions import (db, login_manager)

def create_app(config_name='development'):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    extentions(app)


    # Import blueprints
    from .blueprints.home import home
    from .blueprints.account import account
    from .blueprints.post import post

    # Register blueprints
    app.register_blueprint(home)
    app.register_blueprint(account)
    app.register_blueprint(post)


    return app


def extentions(app):
    #loads the extentions
    db.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'account.login'
    login_manager.init_app(app)

    #recreate_db(app)

    #create db
    #with app.app_context():
        #from .models import User, Post, Comment, Tag, tags
        #db.create_all()
        #bob = User(username="bob", email="bob@gmail.com", password="123")
        #bob.save()
        #db.drop_all()

    return None

######## TESTING STUFF
def create_users():
    from .models import User

    users = [User(username='bob', email='bob@gmail.com', password='123')]

    for user in users:
        user.save()        



def recreate_db(db, app):
    with app.app_context():
        db.drop_all()
        from .models import User
        db.create_all()
        create_users()
