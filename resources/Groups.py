from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from models.ClassGroupModel import ClassGroupModel
from schemas.ClassGroupSchema import ClassGroupSchema
from models.LabGroupModel import LabGroupModel
from schemas.LabGroupSchema import LabGroupSchema
from flask_jwt_extended import jwt_required

class_schema = ClassGroupSchema()
lab_schema = LabGroupSchema()

class ClassGroup(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            class_data = class_schema.load(json_data)
        except ValidationError as error:
            return error.messages
        data = ClassGroupModel(**class_data)
        try:
            data.save_data()
        except IntegrityError as error:
            return error._message(IndentationError)
        return class_schema.dump(data)


class LabGroup(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            lab_data = lab_schema.load(json_data)
        except ValidationError as error:
            return error.messages
        data = LabGroupModel(**lab_data)
        try:
            data.save_data()
        except IntegrityError as error:
            return error._message(IndentationError)
        return lab_schema.dump(data)