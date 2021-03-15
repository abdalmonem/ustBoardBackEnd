from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import api
from .. import db
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
@jwt_required
@supervisor_required
def get_material(title):
    try:
        material = Materials.find_by_title(title)
    except IntegrityError as error:
        return error._message()
    if not material:
        return {"msg": "not found"}, 404
    material_data = material_schema.dump(material)
    return {"data:": material_data}

@api.route('/material/edit/<int:id>', methods=['PUT'])
@jwt_required
@supervisor_required
def edit_material(id):
    json_data = request.get_json()
    try:
        material = Materials.find_by_id(id)
    except IntegrityError as error:
        return error._message()
    if not material:
        return {"msg": "not found"}, 404
    try:
        material_data = material_schema.dump(material)
    except ValidationError as error:
        return error.messages, 400
    try:
        if 'title' in json_data:
            if Materials.query.filter_by(title=json_data['title']).first():
                return {"msg": "material already exists."}, 500
            material.title = json_data['title']
        if 'h_rate' in json_data:
            material.h_rate = json_data['h_rate']
        if 'teacher_id' in json_data:
            material.teacher_id = json_data['teacher_id']
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    try:
        material = Materials.find_by_id(id)
        material_data = material_schema.dump(material)
    except ValidationError as error:
        return error.messages, 400
    return {"msg": "data has been updated.", "data": material_data}

@api.route('/material/delete/<int:id>', methods=['DELETE'])
@jwt_required
@supervisor_required
def delete_material(id):
    try:
        material = Materials.find_by_id(id)
    except IntegrityError as error:
        return error._message()
    if not material:
        return {"msg": "not found"}, 404
    try:
        material.delete_data()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    return {"msg": "material data has been deleted."}

@api.route('/material/all', methods=['GET'])
@jwt_required
@supervisor_required
def get_materials():
    pass
