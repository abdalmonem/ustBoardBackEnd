from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import api
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
    data = LabGroup(**lab_data)
    try:
        data.save_data()
    except IntegrityError as error:
        raise error._message(IndentationError)
    return lab_schema.dump(data)

@api.route('/group/class/<string:group_name>', methods=['GET'])
def get_class_group(group_name):
    pass

@api.route('/group/lab/add/<string:group_name>', methods=['GET'])
def get_lab_group(id):
    pass

@api.route('/group/class/edit/<string:group_name>', methods=['POST'])
def edit_class_group(id):
    pass

@api.route('/group/lab/edit/<string:group_name>', methods=['POST'])
def edit_lab_group(labname):
    pass

@api.route('/group/class/delete/<string:group_name>', methods=['DELETE'])
def delete_class_group(id):
    pass

@api.route('/group/lab/delete/<string:group_name>', methods=['DELETE'])
def delete_lab_group(group_name):
    pass

@api.route('/group/class/all', methods=['GET'])
def get_class_groups():
    pass

@api.route('/group/lab/all', methods=['GET'])
def get_lab_groups():
    pass
