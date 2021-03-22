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
    if request.method == 'POST':
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
    return {"msg": "invalid link"}

@api.route('/student/<int:id>', methods=['GET'])
@jwt_required
@supervisor_required
def get_student(id):
    try:
        student = Student.find_by_id(id)
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
    if request.method == 'PUT' or request.method == 'POST':
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
    return {"msg": "invalid link"}, 400

@api.route('/student/delete/<int:id>', methods=['DELETE'])
@jwt_required
@supervisor_required
def delete_student(id):
    if request.method == 'DELETE':
        try:
            student = Student.find_by_id(id)
        except IntegrityError as error:
            return error._message()
        if not student:
            return {"msg": "not found"}, 404
        try:
            student.delete_data()
        except IntegrityError as error:
            db.session.rollback()
            return error._message(), 500
        return {"msg": "data has been deleted."}
    return {"msg": "invalid link"}, 400

@api.route('/student/all', methods=['GET'])
def get_students():
    if request.args and request.method == 'GET':
        start = int(request.args.get('start'))
        end = int(request.args.get('end'))
        amount = int(request.args.get('amount'))
        page_num = int(request.args.get('page_num'))
        total = Student.get_row_count()
        if (total / amount) % 2 == 0:
            pages = round(total / amount)
        else:
            pages = round(total / amount)
        if page_num == 1:
            data = Student.query.with_entities(
                Student.username, Student.surename, Student.dept_id, Student.card_id
            ).limit(amount)
            if page_num == pages or page_num > pages:
                next_url = ''
            else:
                start = end + 1
                end = end + amount
                page_num = page_num + 1
                next_url = '/student/all?start={}&end={}&amount={}&page_num={}'.format(start, end, amount, page_num)
            return {"next_url": next_url, "Students data": student_schema.dump(data, many=True)}
        elif page_num > 1 and page_num == pages:
            data = Student.query.with_entities(
                Student.username, Student.surename, Student.dept_id, Student.card_id
            ).limit(amount).offset(start - 1)
            if page_num == pages or page_num > pages:
                next_url = ''
            else:
                start = end + 1
                end = end + amount
                page_num = page_num + 1
                next_url = '/student/all?start={}&end={}&amount={}&page_num={}'.format(start, end, amount, page_num)
            return {"next_url": next_url, "Students data": student_schema.dump(data, many=True)}
        else:
            return {"msg": "invalid"}
    return {"msg": "not found."}, 404
