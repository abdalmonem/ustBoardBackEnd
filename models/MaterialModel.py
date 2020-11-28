from flask import Flask
from extensions import db
from models.DepartmentModel import DepartmentModel
from models.UserModel import UserModel


class MaterialModel(db.Model):

    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    hours_rate = db.Column(db.Integer)
    department: DepartmentModel = db.relationship(DepartmentModel)
    department_id = db.Column(db.Integer, db.ForeignKey(DepartmentModel.id), nullable=True)
    year = db.Column(db.Integer)

    @staticmethod
    def init():
        db.create_all()
        print("materials table created")

    @staticmethod
    def drop():
        db.drop_all()
        print("materials table droped")