from flask import request
from flask_jwt_extended import jwt_required
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

@api.route('/department/<int:id>', methods=['GET'])
@jwt_required
@admin_required
def get_department(id):
    try:
        dept = DeptModel.find_by_id(id)
    except IntegrityError as error:
        return error._message()
    if not dept:
        return {"msg": "not found"}, 404
    dept_data = dept_schema.dump(dept)
    return {"data:": dept_data}

@api.route('/department/edit/<int:id>', methods=['PUT'])
@jwt_required
@admin_required
def edit_department(id):
    json_data = request.get_json()
    try:
        dept = DeptModel.find_by_id(id)
    except IntegrityError as error:
        return error._message()
    if not dept:
        return {"msg": "not found"}, 404
    try:
        if 'dept_title' in json_data:
            if DeptModel.query.filter_by(title=json_data['dept_type']).first():
                return {"msg": "department already exists"}, 500
            dept.title = json_data['dept_title']
        if 'dept_type' in json_data:
            dept.type = json_data['dept_type']
        if 'year' in json_data:
            dept.year = json_data['year']
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    try:
        dept = DeptModel.find_by_id(id)
        dept_data = dept_schema.dump(dept)
    except ValidationError as error:
        return error.messages, 400
    return {"msg": "data has been updated.", "data": dept_data}

@api.route('/department/delete/<int:id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_department(id):
    try:
        dept = DeptModel.find_by_id(id)
    except IntegrityError as error:
        return error._message()
    if not dept:
        return {"msg": "not found"}, 404
    try:
        dept.delete_data()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    return {"msg": "department data has been deleted."}

@api.route('/department/all', methods=['GET'])
def get_departments():
    pass
