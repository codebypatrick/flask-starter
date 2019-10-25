from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

from .config import config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    initialize_extensions(app)
    register_blueprints(app)

    return app

def initialize_extensions(app):
    db.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    mail.init_app(app)

def register_blueprints(app):
    from .errors import errors
    from .main import main
    from .auth import auth
    from .post import post

    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(post)
