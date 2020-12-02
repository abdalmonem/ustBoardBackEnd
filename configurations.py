import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
# from models.UsersModel import Users

# App Inistance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'willbechangedlateron'

# Database config "initial config"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
jwt = JWTManager(app)
Migrate(app, db)


@jwt.user_claims_loader
def user_claims(identity):
    if identity == 0:
        return {'is_student': True}
    elif identity == 1:
        return {'is_supervisor': True}
    elif identity == 2:
        return {'is_admin': True}

