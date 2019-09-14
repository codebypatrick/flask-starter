from flask import Flask

from .config import config
from .extentions import db, login_manager

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

    return None
