from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from models.StudentModel import Student
from schemas.StudentSchema import StudentSchema
from flask_jwt_extended import jwt_required


student_schema = StudentSchema()

# Still got other classes to implement
class AddStudent(Resource):

    @jwt_required
    def post(self):
        json_data = request.get_json()
        try:
            data = student_schema.load(json_data)
        except ValidationError as error:
            return error.messages
        student = Student.find_by_phone(data['phone'])
        if student:
            return { "message": "student already exsists." }
        student = Student(**data)
        try:
            student.save_data()
        except IntegrityError as error:
            return error._message(IndentationError)
        return student_schema.dump(student)
            
