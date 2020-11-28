from flask import Flask
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from extensions import db
from models.UserModel import UserModel
from models.ClassGroupModel import ClassGroupModel
from models.DepartmentModel import DepartmentModel
from models.LabGroupModel import LabGroupModel


class StudentModel(db.Model):

    __tablename__ = 'students'
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #
    # @declared_attr
    # def user_id(cls):
    #     return db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=True)
    #
    # @declared_attr
    # def user(cls):
    #     return db.relationship(UserModel)
    # year = db.Column(db.Integer)
    #
    # @declared_attr
    # def department(cls):
    #     return db.relationship(DepartmentModel)
    #
    # @declared_attr
    # def department_id(cls):
    #     return db.Column(db.Integer, db.ForeignKey(DepartmentModel.id), nullable=True)
    #
    # @declared_attr
    # def class_group(cls):
    #     return db.relationship(ClassGroupModel)
    #
    # @declared_attr
    # def class_group_id(cls):
    #     return  db.Column(db.Integer, db.ForeignKey(ClassGroupModel.id), nullable=True)
    #
    # @declared_attr
    # def lab_group(cls):
    #     return db.relationship(LabGroupModel)
    #
    # @declared_attr
    # def lab_group_id(cls):
    #     return db.Column(db.Integer, db.ForeignKey(LabGroupModel.id), nullable=True)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=True)
    user = db.relationship(UserModel)
    year = db.Column(db.Integer)
    department = db.relationship(DepartmentModel)
    department_id = db.Column(db.Integer, db.ForeignKey(DepartmentModel.id), nullable=True)
    class_group = db.relationship(ClassGroupModel)
    class_group_id = db.Column(db.Integer, db.ForeignKey(ClassGroupModel.id), nullable=True)
    lab_group = db.relationship(LabGroupModel)
    lab_group_id = db.Column(db.Integer, db.ForeignKey(LabGroupModel.id), nullable=True)
    
    @staticmethod
    def init():
        db.create_all()
        print("students table created")

    @staticmethod
    def drop():
        db.drop_all()
        print("students table droped")