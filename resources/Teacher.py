from flask import request
from configurations import jwt
from flask_restful import Resource
from models.TeacherModel import Teachers
from schemas.TeacherSchema import TeacherSchema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

teacher_schema = TeacherSchema()


class Teacher(Resource):
    @jwt_required
    def post(self):
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