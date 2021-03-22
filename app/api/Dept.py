from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import api
from .. import db
from .decorators import admin_required
from ..models import DeptModel
from ..schemas import DeptSchema

dept_schema = DeptSchema()

@api.route('/department/add', methods=['POST'])
@jwt_required
@admin_required
def add_department():
    json_data = request.get_json()
    if request.method == 'POST':
        try:
            dept_data = dept_schema.load(json_data)
        except ValidationError as error:
            return error.messages, 400
        dept = DeptModel.check_dept(dept_data['title'], dept_data['dept_type'], year=dept_data['year'])
        if dept:
                return {"message": "Dept already exists."}
        dept = DeptModel(**json_data)
        try:
            dept.save_data()
        except IntegrityError as error:
            return error._message(IndentationError), 500
        return dept_schema.dump(dept)
    return {"msg": "invalid link"}

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
        if 'title' in json_data:
            if DeptModel.query.filter_by(title=json_data['title']).first():
                return {"msg": "department already exists"}, 500
            dept.title = json_data['title']
        if 'dept_type' in json_data:
            dept.dept_type = json_data['dept_type']
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
    return {"msg": "data has been deleted."}

@api.route('/department/all', methods=['GET'])
def get_departments():
    if request.args and request.method == 'GET':
        start = int(request.args.get('start'))
        end = int(request.args.get('end'))
        amount = int(request.args.get('amount'))
        page_num = int(request.args.get('page_num'))
        total = DeptModel.get_row_count()
        if (total / amount) % 2 == 0:
            pages = round(total / amount)
        else:
            pages = round(total / amount) + 1
        if page_num == 1:
            data = DeptModel.query.with_entities(
                DeptModel.title, DeptModel.year, DeptModel.dept_type
            ).limit(amount)
            if page_num == pages or page_num > pages:
                next_url = ''
            else:
                start = end + 1
                end = end + amount
                page_num = page_num + 1
                next_url = '/department/all?start={}&end={}&amount={}&page_num={}'.format(start, end, amount, page_num)
            return {"next_url": next_url, "departments data": dept_schema.dump(data, many=True)}
        elif page_num > 1:
            data = DeptModel.query.with_entities(
                DeptModel.title, DeptModel.year, DeptModel.dept_type
            ).limit(amount).offset(start - 1)
            if page_num == pages or page_num > pages:
                next_url = ''
            else:
                start = end + 1
                end = end + amount
                page_num = page_num + 1
                next_url = '/department/all?start={}&end={}&amount={}&page_num={}'.format(start, end, amount, page_num)
            return {"next_url": next_url, "departments data": dept_schema.dump(data, many=True)}
        else:
            return {"msg": "invalid link"}
    return {"msg": "not found."}, 404
