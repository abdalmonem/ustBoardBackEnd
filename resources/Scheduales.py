from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from models.SchedualeModel import SchedualeModel
from models.ClassScheduale import ClassSchedualeModel
from models.LabSchedualeModel import LabSchedualeModel
from schemas.LabSchedualeSchema import LabSchedualSchema
from schemas.ClassSchedualeSchema import ClassSchedualSchema
from flask_jwt_extended import jwt_required

class_schud_schema = ClassSchedualSchema()
lab_schud_schema = LabSchedualSchema()

class ClassScheduales(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            class_data = class_schud_schema.load(json_data)
        except ValidationError as error:
            return error.messages
        data = ClassSchedualeModel(**class_data)
        try:
            data.save_data()
        except IntegrityError as error:
            return error._message(IndentationError)
        return class_schud_schema.dump(data)


class LabScheduales(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            lab_data = lab_schud_schema.load(json_data)
        except ValidationError as error:
            return error.messages
        data = LabSchedualeModel(**lab_data)
        try:
            data.save_data()
        except IntegrityError as error:
            return error._message(IndentationError)
        return lab_schud_schema.dump(data)