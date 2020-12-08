from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from models.MaterialModel import Materials
from schemas.MaterialSchema import MaterialSchema
from flask_jwt_extended import jwt_required

material_schema = MaterialSchema()

class Material(Resource):
    @jwt_required
    def post(self):
        json_data = request.get_json()
        try:
            material_data = material_schema.load(json_data)
        except ValidationError as error:
            return error.messages
        material = Materials.check_material(material_data['title'])
        if material:
            return {"message": "Material already exists."}
        material = Materials(**json_data)
        try:
            material.save_data()
        except IntegrityError as error:
            return error._message(IndentationError)
        return material_schema.dump(material)

