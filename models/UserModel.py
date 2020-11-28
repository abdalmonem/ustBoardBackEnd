from flask_sqlalchemy import SQLAlchemy
from extensions import db


class DbOperationsHelper:
    _row = None
    db_obj = None

    def __init__(self, row=None, db_obj=None):
        self._row = row
        self.db_obj = db_obj

    def add(self):
        self.db_obj.session.add(self._row)
        self.db_obj.session.commit()

    def modify(self):
        self.db_obj.query.session.commit()

    def remove(self):
        self.db_obj.session.delete(self._row)
        self.db_obj.session.commit()

    def flush(self):
        self.db_obj.session.flush()

    def close(self):
        self.db_obj.session.close()


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20), unique=True)
    date = db.Column(db.Integer)
    thumb = db.Column(db.String(50))
    name = db.Column(db.String(40))
    rank = db.Column(db.Integer)
    auth_key = db.Column(db.String(90))

    @staticmethod
    def init():
        db.create_all()
        print("user table created")

    @staticmethod
    def drop():
        db.drop_all()
        print("user table droped")
