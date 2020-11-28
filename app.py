from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
import os
from api.auth import auth
from api.testfun import testfun
from extensions import db


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost/ustBoard"

app.register_blueprint(auth)
app.register_blueprint(testfun)
db.init_app(app)

if __name__ == '__main__':
    app.run(debug = True)
