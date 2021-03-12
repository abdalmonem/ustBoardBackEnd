import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some hard secret key here'
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UST_ADMIN = os.environ.get('UST_ADMIN')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    SMTP_SERVER = 'smtp.gmail.com'
    PORT = 587
    UST_MAIL = os.environ.get('UST_MAIL')  # 'ust.table@gmail.com'
    UST_PASSWORD = os.environ.get('UST_PASSWORD')  # 'ust@ust200'
    ADMIN_RANK = 3
    SUPERVISOR_RANK = 2
    TEACHER_RANK = 1
    STUDENT_RANK = 0

    @staticmethod
    def init_app(cls,app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    # def init_app(cls, app):
        # DevelopmentConfig.init_app(app)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SSL_REDIRECT = True if os.environ.get('DYNO') else False

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
