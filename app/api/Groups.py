from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import api
from .. import db
from .decorators import supervisor_required
from ..models import ClassGroup
from ..schemas import ClassGroupSchema
from ..models import LabGroup
from ..schemas import LabGroupSchema
from flask_jwt_extended import jwt_required

class_schema = ClassGroupSchema()
lab_schema = LabGroupSchema()

@api.route('/group/class/add', methods=['POST'])
@jwt_required
@supervisor_required
def add_class_group():
    json_data = request.get_json()
    try:
        class_data = class_schema.load(json_data)
    except ValidationError as error:
        raise error.messages
    group = ClassGroup.find_by_name(json_data['group_name'])
    if group:
        return {"msg": "group already exists."}, 500
    data = ClassGroup(**class_data)
    try:
        data.save_data()
    except IntegrityError as error:
        raise error._message(IndentationError)
    return class_schema.dump(data)

@api.route('/group/lab/add', methods=['POST'])
@jwt_required
@supervisor_required
def add_lab_group():
    json_data = request.get_json()
    try:
        lab_data = lab_schema.load(json_data)
    except ValidationError as error:
        raise error.messages
    lab = LabGroup.find_by_name(json_data['group_name'])
    if lab:
        return {"msg": "group already exists."}, 500
    data = LabGroup(**lab_data)
    try:
        data.save_data()
    except IntegrityError as error:
        raise error._message(IndentationError)
    return lab_schema.dump(data)

@api.route('/group/class/<string:group_name>', methods=['GET'])
@jwt_required
@supervisor_required
def get_class_group(group_name):
    try:
        class_group = ClassGroup.find_by_name(group_name)
    except IntegrityError as error:
        return error._message()
    if not class_group:
        return {"msg": "not found"}, 404
    group_data = class_schema.dump(class_group)
    return {"data:": group_data}

@api.route('/group/lab/add/<string:group_name>', methods=['GET'])
@jwt_required
@supervisor_required
def get_lab_group(lab_name):
    try:
        lab_group = LabGroup.find_by_name(lab_name)
    except IntegrityError as error:
        return error._message()
    if not lab_group:
        return {"msg": "not found"}, 404
    group_data = lab_schema.dump(lab_group)
    return {"data:": group_data}

@api.route('/group/class/edit/<int:id>', methods=['PUT'])
@jwt_required
@supervisor_required
def edit_class_group(id):
    json_data = request.get_json()
    try:
        class_group = ClassGroup.find_by_id(id)
    except IntegrityError as error:
        return error._message()
    if not class_group:
        return {"msg": "not found"}, 404
    try:
        if 'group_name' in json_data:
            if ClassGroup.query.filter_by(group_name=json_data['group_name']).first():
                return {"msg": "class group already exists."}, 500
            class_group.group_name = json_data['group_name']
        if 'hall_number' in json_data:
            class_group.hall_number = json_data['hall_number']
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    try:
        class_group = ClassGroup.find_by_id(id)
        class_data = class_schema.dump(class_group)
    except ValidationError as error:
        return error.messages, 400
    return {"msg": "data has been updated.", "data": class_data}

@api.route('/group/lab/edit/<int:id>', methods=['PUT'])
@jwt_required
@supervisor_required
def edit_lab_group(id):
    json_data = request.get_json()
    try:
        lab_group = LabGroup.find_by_id(id)
    except IntegrityError as error:
        return error._message()
    if not lab_group:
        return {"msg": "not found"}, 404
    try:
        if 'group_name' in json_data:
            if LabGroup.query.filter_by(group_name=json_data['group_name']).first():
                return {"msg": "class group already exists."}, 500
            lab_group.group_name = json_data['group_name']
        if 'center_number' in json_data:
            lab_group.center_number = json_data['center_number']
        if 'lab_number' in json_data:
            lab_group.lab_number = json_data['lab_number']
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    try:
        lab_group = LabGroup.find_by_id(id)
        lab_data = lab_schema.dump(lab_group)
    except ValidationError as error:
        return error.messages, 400
    return {"msg": "data has been updated.", "data": lab_data}

@api.route('/group/class/delete/<string:group_name>', methods=['DELETE'])
@jwt_required
@supervisor_required
def delete_class_group(group_name):
    try:
        class_group = ClassGroup.find_by_name(group_name)
    except IntegrityError as error:
        return error._message()
    if not class_group:
        return {"msg": "not found"}, 404
    try:
        class_group.delete_data()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    return {"msg": "data has been deleted."}

@api.route('/group/lab/delete/<string:group_name>', methods=['DELETE'])
@jwt_required
@supervisor_required
def delete_lab_group(group_name):
    try:
        lab_group = LabGroup.find_by_name(group_name)
    except IntegrityError as error:
        return error._message()
    if not lab_group:
        return {"msg": "not found"}, 404
    try:
        lab_group.delete_data()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    return {"msg": "data has been deleted."}

@api.route('/group/class/all', methods=['GET'])
@jwt_required
@supervisor_required
def get_class_groups():
    pass

@api.route('/group/lab/all', methods=['GET'])
@jwt_required
@supervisor_required
def get_lab_groups():
    pass
