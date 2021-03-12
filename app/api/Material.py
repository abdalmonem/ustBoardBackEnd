from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import api
from .decorators import supervisor_required
from ..models import Materials
from ..schemas import MaterialSchema
from flask_jwt_extended import jwt_required

material_schema = MaterialSchema()

@api.route('/material/add', methods=['POST'])
@jwt_required
@supervisor_required
def add_material():
    json_data = request.get_json()
    try:
        material_data = material_schema.load(json_data)
    except ValidationError as error:
        return error.messages, 400
    material = Materials.check_material(material_data['title'])
    if material:
        return {"message": "Material already exists."}
    material = Materials(**json_data)
    try:
        material.save_data()
    except IntegrityError as error:
        return error._message(IndentationError), 500
    return material_schema.dump(material)

@api.route('/material/<string:title>', methods=['GET'])
def get_material(title):
    pass

@api.route('/material/edit/<string:title>', methods=['POST'])
def edit_material(title):
    pass

@api.route('/material/delete/<string:title>', methods=['DELETE'])
def delete_material(title):
    pass

@api.route('/material/all', methods=['GET'])
def get_materials():
    pass
