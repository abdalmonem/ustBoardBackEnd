from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from .decorators import supervisor_required
from . import api
from .. import db
from .. import jwt
from ..models import Teachers
from ..schemas.TeacherSchema import TeacherSchema

teacher_schema = TeacherSchema()

@api.route('/teacher/add', methods=['POST'])
@jwt_required
@supervisor_required
def add_teacher():
    if request.method == 'POST':
        json_data = request.get_json()
        try:
            data = teacher_schema.load(json_data)
        except ValidationError as error:
            return error.messages
        teacher = Teachers.find_by_phone(data['phone'])
        if teacher:
            return {"message": "Teacher already exists."}
        teacher = Teachers(**data)
        try:
            teacher.save_data()
        except IntegrityError as error:
            return error._message(IndentationError)
        return teacher_schema.dump(teacher)
    return {"msg": "invalid link"}

@api.route('/teacher/<int:id>', methods=['GET'])
@jwt_required
@supervisor_required
def get_teacher(id):
    if request.method == 'GET':
        try:
            teacher = Teachers.find_by_id(id)
        except:
            return {"msg": "Database error."}
        if teacher:
            return {"data": teacher_schema.dump(teacher)}
        return {"msg": "User not found."}, 404
    return {"msg": "invalid link"}, 400

@api.route('/teacher/edit/<int:id>', methods=['PUT'])
@jwt_required
@supervisor_required
def edit_teacher(id):
    json_data = request.get_json()
    try:
        teacher = Teachers.find_by_id(id)
    except IntegrityError as error:
        return error._message()
    if not teacher:
        return {"msg": "not found"}, 404
    try:
        teacher_data = teacher_schema.dump(teacher)
    except ValidationError as error:
        return error.messages, 400
    try:
        if 'email' in json_data:
            if Teachers.query.filter_by(email=json_data['email']).first():
                return {"msg": "email already exists"}, 500
            teacher.email = json_data['email']

        if 'phone' in json_data:
            if Teachers.find_by_phone(json_data['phone']):
                return {"msg": "phone already exists"}, 500
            teacher.phone = json_data['phone']

        if 'username' in json_data:
            if Teachers.find_by_username(json_data['username']):
                return {"msg": "username already token"}
            teacher.username = json_data['username']
        if 'teacher_card' in json_data:
            if Teachers.query.filter_by(card_id=json_data['card_id']).first():
                return {"msg": "card number can't be deprecated."}
            teacher.card_id = json_data['card_id']
        
        if 'surename' in json_data:
            teacher.surename = json_data['surename']
        if 'gendre' in json_data:
            teacher.gendre = json_data['gendre']
        if 'year' in json_data:
            teacher.year = json_data['year']
        if 'password' in json_data:
            return {"msg": "unautherized action, only the account user can edit his password"}
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    try:
        teacher = Teachers.find_by_id(id)
        teacher_data = teacher_schema.dump(teacher)
    except ValidationError as error:
        return error.messages, 400
    return {"msg": "data has been updated.", "data": teacher_data}

@api.route('/teacher/delete/<int:id>', methods=['DELETE'])
@jwt_required
@supervisor_required
def delete_teacher(id):
    if request.method == 'DELETE':
        try:
            teacher = Teachers.find_by_id(id)
        except IntegrityError as error:
            return error._message()
        if not teacher:
            return {"msg": "not found"}, 404
        try:
            teacher.delete_data()
        except IntegrityError as error:
            db.session.rollback()
            return error._message(), 500
        return {"msg": "data has been deleted."}
    return {"msg": "invalid link"}, 400

@api.route('/teacher/all', methods=['GET'])
@jwt_required
@supervisor_required
def get_teachers():
    if request.args and request.method == 'GET':
        start = int(request.args.get('start'))
        end = int(request.args.get('end'))
        amount = int(request.args.get('amount'))
        page_num = int(request.args.get('page_num'))
        total = Teachers.get_row_count()
        if (total / amount) % 2 == 0:
            pages = round(total / amount)
        else:
            pages = round(total / amount)
        if page_num == 1:
            data = Teachers.query.with_entities(
                Teachers.username, Teachers.surename, Teachers.teacher_card
            ).limit(amount)
            if page_num == pages or page_num > pages:
                next_url = ''
            else:
                start = end + 1
                end = end + amount
                page_num = page_num + 1
                next_url = '/teacher/all?start={}&end={}&amount={}&page_num={}'.format(start, end, amount, page_num)
            return {"next_url": next_url, "Teacher data": teacher_schema.dump(data, many=True)}
        elif page_num > 1:
            data = Teachers.query.with_entities(
                Teachers.username, Teachers.surename, Teachers.teacher_card
            ).limit(amount).offset(start - 1)
            if page_num == pages or page_num > pages:
                next_url = ''
            else:
                start = end + 1
                end = end + amount
                page_num = page_num + 1
                next_url = '/teacher/all?start={}&end={}&amount={}&page_num={}'.format(start, end, amount, page_num)
            return {"next_url": next_url, "Teacher data": teacher_schema.dump(data, many=True)}
        else:
            return {"msg": "invalid link"}, 400
    return {"msg": "not found."}, 404
