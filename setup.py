from flask import Flask
from app import app
from extensions import db
import inspect
import pyclbr

from models.ClassGroupModel import ClassGroupModel
from models.DepartmentModel import DepartmentModel
from models.LabGroupModel import LabGroupModel
from models.MaterialModel import MaterialModel
from models.SchedulesModel import SchedulesModel
from models.UserModel import UserModel
from models.StudentModel import StudentModel

password = input('Enter setup password:')
if password == "abc":
    # ما عارف دا شنو
    with app.app_context():
        print("initializing ...")
        UserModel.drop()
        UserModel.init()

        StudentModel.drop()
        StudentModel.init()

        DepartmentModel.drop()
        DepartmentModel.init()

        ClassGroupModel.drop()
        ClassGroupModel.init()

        LabGroupModel.drop()
        LabGroupModel.init()

        MaterialModel.drop()
        MaterialModel.init()

        SchedulesModel.drop()
        SchedulesModel.init()
else:
    print("incorrect password")
