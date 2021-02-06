from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import api
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
def get_student(username):
    pass

@api.route('/student/edit/<string:username>', methods=['POST'])
def edit_student(username):
    pass

@api.route('/student/delete/<string:username>', methods=['DELETE'])
def delete_student(username):
    pass

@api.route('/student/all', methods=['GET'])
def get_students():
    pass
