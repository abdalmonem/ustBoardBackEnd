from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from config import config
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    ma.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/main/v1')

    return app
