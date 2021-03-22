from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import api
from .. import db
from .decorators import supervisor_required
from ..schemas import ClassSchedualSchema, ClassGroupSchema, LabSchedualSchema, LabGroupSchema
from ..models import LabGroup, ClassGroup
from flask_jwt_extended import jwt_required

class_schema = ClassGroupSchema()
lab_schema = LabGroupSchema()

@api.route('/group/class/add', methods=['POST'])
@jwt_required
@supervisor_required
def add_class_group():
    json_data = request.get_json()
    if request.method == 'POST':
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
    return {"msg": "invalid link"}, 400

@api.route('/group/lab/add', methods=['POST'])
@jwt_required
@supervisor_required
def add_lab_group():
    json_data = request.get_json()
    if request.method == 'POST':
        try:
            lab_data = lab_schema.load(json_data)
        except ValidationError as error:
            return error.messages
        lab = LabGroup.find_by_name(json_data['group_name'])
        if lab:
            return {"msg": "group already exists."}, 500
        data = LabGroup(**lab_data)
        try:
            data.save_data()
        except IntegrityError as error:
            return error._message(IndentationError)
        return lab_schema.dump(data)
    return {"msg": "invalid link"}, 400

@api.route('/group/class/<int:id>', methods=['GET'])
@jwt_required
@supervisor_required
def get_class_group(id):
    if request.method == 'GET':
        try:
            class_group = ClassGroup.find_by_id(id)
        except IntegrityError as error:
            return error._message()
        if not class_group:
            return {"msg": "not found"}, 404
        group_data = class_schema.dump(class_group)
        return {"data:": group_data}
    return {"msg": "invalid link"}, 400

@api.route('/group/lab/<int:id>', methods=['GET'])
@jwt_required
@supervisor_required
def get_lab_group(id):
    if request.method == 'GET':
        try:
            lab_group = LabGroup.find_by_id(id)
        except IntegrityError as error:
            return error._message()
        if not lab_group:
            return {"msg": "not found"}, 404
        group_data = lab_schema.dump(lab_group)
        return {"data:": group_data}
    return {"msg": "invalid link"}, 400

@api.route('/group/class/edit/<int:id>', methods=['PUT'])
@jwt_required
@supervisor_required
def edit_class_group(id):
    json_data = request.get_json()
    if request.method == 'PUT' or request.method == 'POST':
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
    return {"msg": "invalid link"}, 400

@api.route('/group/lab/edit/<int:id>', methods=['PUT'])
@jwt_required
@supervisor_required
def edit_lab_group(id):
    json_data = request.get_json()
    if request.method == 'PUT' or request.method == 'POST':
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
    return {"msg": "invalid link"}, 400

@api.route('/group/class/delete/<int:id>', methods=['DELETE'])
@jwt_required
@supervisor_required
def delete_class_group(id):
    if request.method == 'DELETE':
        try:
            class_group = ClassGroup.find_by_id(id)
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
    return {"msg": "invalid link"}, 400

@api.route('/group/lab/delete/<int:id>', methods=['DELETE'])
@jwt_required
@supervisor_required
def delete_lab_group(id):
    if request.method == 'DELETE':
        try:
            lab_group = LabGroup.find_by_id(id)
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
    return {"msg": "invalid link"}, 400

@api.route('/group/class/all', methods=['GET'])
@jwt_required
@supervisor_required
def get_class_groups():
    if request.args and request.method == 'GET':
        start = int(request.args.get('start'))
        end = int(request.args.get('end'))
        amount = int(request.args.get('amount'))
        page_num = int(request.args.get('page_num'))
        total = ClassGroup.get_row_count()
        if (total / amount) % 2 == 0:
            pages = round(total / amount)
        else:
            pages = round(total / amount) + 1
        if page_num == 1:
            data = ClassGroup.query.with_entities(
                ClassGroup.group_name, ClassGroup.hall_number, ClassGroup.dept_id
            ).limit(amount)
            if page_num == pages or page_num > pages:
                next_url = ''
            else:
                start = end + 1
                end = end + amount
                page_num = page_num + 1
                next_url = '/group/class/all?start={}&end={}&amount={}&page_num={}'.format(start, end, amount, page_num)
            return {"next_url": next_url, "class data": class_schema.dump(data, many=True)}
        elif page_num > 1:
            data = ClassGroup.query.with_entities(
                ClassGroup.group_name, ClassGroup.hall_number, ClassGroup.dept_id
            ).limit(amount).offset(start - 1)
            if page_num == pages or page_num > pages:
                next_url = ''
            else:
                start = end + 1
                end = end + amount
                page_num = page_num + 1
                next_url = '/group/class/all?start={}&end={}&amount={}&page_num={}'.format(start, end, amount, page_num)
            return {"next_url": next_url, "class group data": class_schema.dump(data, many=True)}
        else:
            return {"msg": "invalid link"}
    return {"msg": "not found."}, 404

@api.route('/group/lab/all', methods=['GET'])
@jwt_required
@supervisor_required
def get_lab_groups():
    if request.args and request.method == 'GET':
        start = int(request.args.get('start'))
        end = int(request.args.get('end'))
        amount = int(request.args.get('amount'))
        page_num = int(request.args.get('page_num'))
        total = LabGroup.get_row_count()
        if (total / amount) % 2 == 0:
            pages = round(total / amount)
        else:
            pages = round(total / amount) + 1
        if page_num == 1:
            data = LabGroup.query.with_entities(
                LabGroup.group_name, LabGroup.center_number, LabGroup.lab_number, LabGroup.dept_id
            ).limit(amount)
            if page_num == pages or page_num > pages:
                next_url = ''
            else:
                start = end + 1
                end = end + amount
                page_num = page_num + 1
                next_url = '/group/lab/all?start={}&end={}&amount={}&page_num={}'.format(start, end, amount, page_num)
            return {"next_url": next_url, "lab group data": lab_schema.dump(data, many=True)}
        elif page_num > 1:
            data = LabGroup.query.with_entities(
                LabGroup.group_name, LabGroup.center_number, LabGroup.lab_number, LabGroup.dept_id
            ).limit(amount).offset(start - 1)
            if page_num == pages or page_num > pages:
                next_url = ''
            else:
                start = end + 1
                end = end + amount
                page_num = page_num + 1
                next_url = '/group/lab/all?start={}&end={}&amount={}&page_num={}'.format(start, end, amount, page_num)
            return {"next_url": next_url, "lab group data": lab_schema.dump(data, many=True)}
        else:
            return {"msg": "invalid link"}
    return {"msg": "not found."}, 404
