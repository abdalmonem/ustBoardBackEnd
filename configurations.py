import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import engine
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager

# App Inistance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'willbechangedlateron'
db_name = 'ustDatabase'
db_user = 'root:'
db_pass = ''
db_addr = '@127.0.0.1/'

# Database config "initial config"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + db_user + db_pass + db_addr + db_name
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

