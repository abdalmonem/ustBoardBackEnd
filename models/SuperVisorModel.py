from flask import Flask

from extensions import db
from models.DepartmentModel import DepartmentModel
from models.UserModel import UserModel


class SuperVisorModel(db.Model):
    __tablename__ = 'supervisors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=True)
    user = db.relationship(UserModel)
    year = db.Column(db.Integer)
    department = db.relationship(DepartmentModel)
    department_id = db.Column(db.Integer, db.ForeignKey(DepartmentModel.id), nullable=True)


    @staticmethod
    def init():
        db.create_all()
        print("supervisors table created")

    @staticmethod
    def drop():
        db.drop_all()
        print("supervisors table droped")