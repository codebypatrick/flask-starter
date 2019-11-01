import os

# Define application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
    DEBUG = True
    SECRET_KEY = 's3cr3t'
    SECURITY_SALT = 's3cr3t-salt'
    TOKEN_VALIDITY = 3600
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'codebypatrick@gmail.com' # os env
    MAIL_DEFAULT_SENDER = 'codebypatrick@gmail.com' # os env
    MAIL_PASSWORD = '@$$patrick2019' # os env


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')


config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,

        'default': DevelopmentConfig
        }
