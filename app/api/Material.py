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
    if request.method == 'POST':
        json_data = request.get_json()
        try:
            material_data = material_schema.load(json_data)
        except ValidationError as error:
            return error.messages, 400
        material = Materials.check_material(json_data['title'], json_data['dept_id'])
        if material:
            return {"message": "Dept already exists."}
        material = Materials(**json_data)
        try:
            material.save_data()
        except IntegrityError as error:
            return error._message(IndentationError), 500
        return material_schema.dump(material)
    return {"msg": "invalid link."}, 400

@api.route('/material/<int:id>', methods=['GET'])
@jwt_required
@supervisor_required
def get_material(id):
    if request.method == 'GET':
        try:
            material = Materials.find_by_id(id)
        except IntegrityError as error:
            return error._message()
        if not material:
            return {"msg": "not found"}, 404
        material_data = material_schema.dump(material)
        return {"data:": material_data}
    return {"msg": "invalid link."}, 400

@api.route('/material/edit/<int:id>', methods=['PUT'])
@jwt_required
@supervisor_required
def edit_material(id):
    if request.method == 'PUT' or request.method == 'POST':
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
    return {"msg": "invalid link."}, 400

@api.route('/material/delete/<int:id>', methods=['DELETE'])
@jwt_required
@supervisor_required
def delete_material(id):
    if request.method == 'DELETE':
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
    return {"msg": "invalid link"}, 400

@api.route('/material/all', methods=['GET'])
@jwt_required
@supervisor_required
def get_materials():
    if request.args and request.method == 'GET':
        start = int(request.args.get('start'))
        end = int(request.args.get('end'))
        amount = int(request.args.get('amount'))
        page_num = int(request.args.get('page_num'))
        total = Materials.get_row_count()
        if (total / amount) % 2 == 0:
            pages = int(round(total / amount))
        else:
            pages = int(round(total / amount))
        print(pages)
        if page_num == 1:
            data = Materials.query.with_entities(
                Materials.title, Materials.h_rate, Materials.dept_id, Materials.teacher_id
            ).limit(amount)
            if page_num == pages or page_num > pages:
                next_url = ''
            else:
                start = end + 1
                end = end + amount
                page_num = page_num + 1
                next_url = '/department/all?start={}&end={}&amount={}&page_num={}'.format(start, end, amount, page_num)
            return {"next_url": next_url, "Materials data": material_schema.dump(data, many=True)}
        elif page_num > 1:
            data = Materials.query.with_entities(
                Materials.title, Materials.h_rate, Materials.dept_id, Materials.teacher_id
            ).limit(amount).offset(start - 1)
            if page_num == pages or page_num > pages:
                next_url = ''
            else:
                start = end + 1
                end = end + amount
                page_num = page_num + 1
                next_url = '/department/all?start={}&end={}&amount={}&page_num={}'.format(start, end, amount, page_num)
            return {"next_url": next_url, "Materials data": material_schema.dump(data, many=True)}
        else:
            return {"msg": "invalid link"}, 400
    return {"msg": "not found."}, 404
