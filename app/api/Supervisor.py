from flask import request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update
from .decorators import admin_required
from . import api
from .. import db
from ..models import Supervisor
from ..schemas.SupervisorSchema import SupervisorSchema
from ..functions.Methods import pagination

supervisor_schema = SupervisorSchema()

@api.route('/supervisor/add', methods=['POST'])
@jwt_required
@admin_required
def add_supervisor():
    json_data = request.get_json()
    if request.method == 'POST':
        try:
            data = supervisor_schema.load(json_data)
        except ValidationError as error:
            return error.messages, 400
        supervisor = Supervisor.find_by_phone(data['phone'])
        if supervisor:
            return {"message": "Supervisor already exists."}
        supervisor = Supervisor(**data)
        try:
            supervisor.save_data()
        except IntegrityError as error:
            return error._message(IndentationError), 500
        return supervisor_schema.dump(supervisor)
    return {"msg": "invalid link"}, 400

@api.route('/supervisor/<int:id>', methods=['GET'])
@jwt_required
@admin_required
def get_supervisor(id):
    if request.method == 'GET':
        try:
            supervisor = Supervisor.find_by_id(id)
        except IntegrityError as error:
            return error._message()
        if not supervisor:
            return {"msg": "not found"}, 404
        supervisor_data = supervisor_schema.dump(supervisor)
        return {"data": supervisor_data}
    return {"msg": "invalid link"}, 400

@api.route('/supervisor/edit/<int:id>', methods=['PUT'])
@jwt_required
@admin_required
def edit_supervisor(id):
    json_data = request.get_json()
    if request.method == 'PUT' or request.method == 'POST':
        try:
            supervisor = Supervisor.find_by_id(id)
        except IntegrityError as error:
            return error._message()
        if not supervisor:
            return {"msg": "not found"}, 404
        try:
            supervisor_data = supervisor_schema.dump(supervisor)
        except ValidationError as error:
            return error.messages, 400
        try:
            if 'email' in json_data:
                if Supervisor.query.filter_by(email=json_data['email']).first():
                    return {"msg": "email already exists"}, 500
                supervisor.email = json_data['email']

            if 'phone' in json_data:
                if Supervisor.find_by_phone(json_data['phone']):
                    return {"msg": "phone already exists"}, 500
                supervisor.phone = json_data['phone']

            if 'username' in json_data:
                if Supervisor.find_by_username(json_data['username']):
                    return {"msg": "username already token"}
                supervisor.username = json_data['username']
            if 'card_id' in json_data:
                if Supervisor.query.filter_by(card_id=json_data['card_id']).first():
                    return {"msg": "card number can't be deprecated."}
                supervisor.card_id = json_data['card_id']
            
            if 'surename' in json_data:
                supervisor.surename = json_data['surename']
            if 'gendre' in json_data:
                supervisor.gendre = json_data['gendre']
            if 'year' in json_data:
                supervisor.year = json_data['year']
            if 'password' in json_data:
                return {"msg": "unautherized action, only the account user can edit his password"}
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            return error._message(), 500
        try:
            supervisor = Supervisor.find_by_id(id)
            supervisor_data = supervisor_schema.dump(supervisor)
        except ValidationError as error:
            return error.messages, 400
        return {"msg": "data has been updated.", "data": supervisor_data}
    return {"msg": "invalid link"}, 400

@api.route('/supervisor/delete/<int:id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_supervisor(id):
    if request.method == 'DELETE':
        try:
            supervisor = Supervisor.find_by_id(id)
        except IntegrityError as error:
            return error._message()
        if not supervisor:
            return {"msg": "not found"}, 404
        try:
            supervisor.delete_data()
        except IntegrityError as error:
            db.session.rollback()
            return error._message(), 500
        return {"msg": "data has been deleted."}
    return {"msg": "invalid link"}, 400

@api.route('/supervisor/all',methods=['GET'])
@jwt_required
@admin_required
def get_supervisors():
    if request.args and request.method == 'GET':
        start = int(request.args.get('start'))
        end = int(request.args.get('end'))
        amount = int(request.args.get('amount'))
        page_num = int(request.args.get('page_num'))
        total = Supervisor.get_row_count()
        if (total / amount) % 2 == 0:
            pages = round(total / amount)
        else:
            pages = round(total / amount)
        if page_num == 1:
            data = Supervisor.query.with_entities(
                Supervisor.username, Supervisor.surename, Supervisor.dept_id, Supervisor.super_card
            ).limit(amount)
            if page_num == pages or page_num > pages:
                next_url = ''
            else:
                start = end + 1
                end = end + amount
                page_num = page_num + 1
                next_url = '/department/all?start={}&end={}&amount={}&page_num={}'.format(start, end, amount, page_num)
            return {"next_url": next_url, "Supervisors data": supervisor_schema.dump(data, many=True)}
        elif page_num > 1:
            data = Supervisor.query.with_entities(
                Supervisor.username, Supervisor.surename, Supervisor.dept_id, Supervisor.super_card
            ).limit(amount).offset(start - 1)
            if page_num == pages or page_num > pages:
                next_url = ''
            else:
                start = end + 1
                end = end + amount
                page_num = page_num + 1
                next_url = '/department/all?start={}&end={}&amount={}&page_num={}'.format(start, end, amount, page_num)
            return {"next_url": next_url, "Supervisors data": supervisor_schema.dump(data, many=True)}
        else:
            return {"msg": "invalid link"}, 400
    return {"msg": "not found."}, 404
