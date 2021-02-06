from flask import request
from flask_jwt_extended import jwt_required, get_jwt_claims
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import api
from .decorators import admin_required
from ..models import DeptModel
from ..schemas import DeptSchema

dept_schema = DeptSchema()

@api.route('/department/add', methods=['POST'])
@jwt_required
@admin_required
def add_department():
    json_data = request.get_json()
    try:
        dept_data = dept_schema.load(json_data)
    except ValidationError as error:
        return error.messages, 400
    dept = DeptModel.check_dept(dept_data['title'], dept_data['dept_type'])
    if dept:
            return {"message": "Dept already exists."}
    dept = DeptModel(**json_data)
    try:
        dept.save_data()
    except IntegrityError as error:
        return error._message(IndentationError), 500
    return dept_schema.dump(dept)

@api.route('/department/<string:title>', methods=['GET'])
def get_department(title):
    pass

@api.route('/department/edit/<string:title>', methods=['POST'])
def edit_department(title):
    pass

@api.route('/department/delete/<string:title>', methods=['DELETE'])
def delete_department(title):
    pass

@api.route('/department/all', methods=['GET'])
def get_departments():
    pass
