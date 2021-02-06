from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from .decorators import supervisor_required
from . import api
from .. import jwt
from ..models import Teachers
from ..schemas.TeacherSchema import TeacherSchema

teacher_schema = TeacherSchema()

@api.route('/teacher/add', methods=['POST'])
@jwt_required
@supervisor_required
def add_teacher():
    json_data = request.get_json()
    try:
        data = teacher_schema.load(json_data)
    except ValidationError as error:
        raise error.messages
    teacher = Teachers.find_by_phone(data['phone'])
    if teacher:
        return {"message": "Teacher already exists."}
    teacher = Teachers(**data)
    try:
        teacher.save_data()
    except IntegrityError as error:
        raise error._message(IndentationError)
    return teacher_schema.dump(teacher)

@api.route('/teacher/<string:username>', methods=['GET'])
def get_teacher(username):
    pass

@api.route('/teacher/edit/<string:username>', methods=['POST'])
def edit_teacher(username):
    pass

@api.route('/teacher/delete/<string:username>', methods=['DELETE'])
def delete_teacher(username):
    pass

@api.route('/admin/all', methods=['GET'])
def get_teachers():
    pass
