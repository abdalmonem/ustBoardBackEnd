from flask import Flask
from extensions import db
from models.ClassGroupModel import ClassGroupModel
from models.DepartmentModel import DepartmentModel
from models.LabGroupModel import LabGroupModel
from models.MaterialModel import MaterialModel
from models.UserModel import UserModel


class SchedulesModel(db.Model):

    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer)
    material: MaterialModel = db.relationship(MaterialModel)
    material_id = db.Column(db.Integer, db.ForeignKey(MaterialModel.id), nullable=True)
    class_group_model: ClassGroupModel = db.relationship(ClassGroupModel)
    class_group_model_id = db.Column(db.Integer, db.ForeignKey(ClassGroupModel.id), nullable=True)
    lab_group_model: LabGroupModel = db.relationship(LabGroupModel)
    lab_group_model_id = db.Column(db.Integer, db.ForeignKey(LabGroupModel.id), nullable=True)
    teacher : UserModel = db.relationship(UserModel)
    teacher_id = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=True)
    position = db.Column(db.Integer)
    day = db.Column(db.String(5))

    @staticmethod
    def init():
        db.create_all()
        print("schedules table created")

    @staticmethod
    def drop():
        db.drop_all()
        print("schedules table droped")