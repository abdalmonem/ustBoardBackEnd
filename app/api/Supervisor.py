from flask import request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update
from .decorators import admin_required
from . import api
from ..models import Supervisor
from ..schemas.SupervisorSchema import SupervisorSchema
from ..functions.Methods import pagination

supervisor_schema = SupervisorSchema()

@api.route('/supervisor/add', methods=['POST'])
@jwt_required
@admin_required
def add_supervisor():
    json_data = request.get_json()
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

@api.route('/supervisor/<string:username>', methods=['GET'])
@jwt_required
@admin_required
def get_supervisor(username):
    try:
        supervisor = Supervisor.find_by_username(username)
    except:
        return {"msg": "Database error."}
    if supervisor:
        return supervisor_schema.dump(supervisor)
    return {"msg": "User not found."}, 404

@api.route('/supervisor/edit/<string:username>', methods=['PUT'])
def edit_supervisor(username):
    pass

@api.route('/supervisor/delete/<string:username>', methods=['DELETE'])
def delete_supervisor(username):
    pass

@api.route('/supervisor/all',methods=['GET'])
def get_supervisors():
    page_num = request.args.get('page_num')
    model_data = supervisor_schema.dump(Supervisor.get_all(), many=True)
    return pagination(model_data, page_num, '/supervisors')


# @api.route('/supervisor', methods=['PUT'])
# @jwt_required
# @admin_required
# def update_supervisor():
#     data = dict(request.args)
#     json_data = request.get_json()
#     try:
#         updated_data = supervisor_schema.load(json_data)
#     except ValidationError as error:
#         return error.messages
#     supervisor = Supervisor.find_by_id(data['id'])
#     if not supervisor:
#         return {"msg": "User not found."}, 404
#     else:
#         supervisor.dept_id = updated_data['dept_id']
#         json_data = supervisor_schema.dump(supervisor)
#     supervisor.save_data()
#     return {"msg": json_data}