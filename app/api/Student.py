from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import api
from .. import db
from .decorators import supervisor_required
from .email import send_verfy_mail
from ..models import Student
from ..schemas.StudentSchema import StudentSchema

student_schema = StudentSchema()

@api.route('/student/add', methods=['POST'])
@jwt_required
@supervisor_required
def add_student():
    json_data = request.get_json()
    try:
        data = student_schema.load(json_data)
    except ValidationError as error:
        return error.messages, 400
    student = Student.find_by_phone(data['phone'])
    if student:
        return { "message": "student already exsists." }
    student = Student(**data)
    try:
        student.save_data()
    except IntegrityError as error:
        return error._message(IndentationError), 500    
    return student_schema.dump(student)

@api.route('/student/<string:username>', methods=['GET'])
@jwt_required
@supervisor_required
def get_student(username):
    try:
        student = Student.find_by_username(username)
    except IntegrityError as error:
        return error._message()
    if not student:
        return {"msg": "not found"}, 404
    student_data = student_schema.dump(student)
    return {"data:": student_data}

@api.route('/student/edit/<int:id>', methods=['PUT'])
@jwt_required
@supervisor_required
def edit_student(id):
    json_data = request.get_json()
    try:
        student = Student.find_by_id(id)
    except IntegrityError as error:
        return error._message()
    if not student:
        return {"msg": "not found"}, 404
    try:
        student_data = student_schema.dump(student)
    except ValidationError as error:
        return error.messages, 400
    try:
        if 'email' in json_data:
            if Student.query.filter_by(email=json_data['email']).first():
                return {"msg": "email already exists"}, 500
            student.email = json_data['email']

        if 'phone' in json_data:
            if Student.find_by_phone(json_data['phone']):
                return {"msg": "phone already exists"}, 500
            student.phone = json_data['phone']

        if 'username' in json_data:
            if Student.find_by_username(json_data['username']):
                return {"msg": "username already token"}
            student.username = json_data['username']
        if 'card_id' in json_data:
            if Student.query.filter_by(card_id=json_data['card_id']).first():
                return {"msg": "card number can't be deprecated."}
            student.card_id = json_data['card_id']
        
        if 'surename' in json_data:
            student.surename = json_data['surename']
        if 'gendre' in json_data:
            student.gendre = json_data['gendre']
        if 'year' in json_data:
            student.year = json_data['year']
        if 'password' in json_data:
            return {"msg": "unautherized action, only the account user can edit his password"}
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    try:
        student = Student.find_by_id(id)
        student_data = student_schema.dump(student)
    except ValidationError as error:
        return error.messages, 400
    return {"msg": "data has been updated.", "data": student_data}

@api.route('/student/delete/<string:username>', methods=['DELETE'])
@jwt_required
@supervisor_required
def delete_student(username):
    try:
        student = Student.find_by_username(username)
    except IntegrityError as error:
        return error._message()
    if not student:
        return {"msg": "not found"}, 404
    try:
        student.delete_data()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    return {"msg": "admin data has been deleted."}

@api.route('/student/all', methods=['GET'])
def get_students():
    pass
