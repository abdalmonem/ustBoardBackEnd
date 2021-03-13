from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required
from .email import send_verfy_mail
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from .decorators import admin_required
from . import api
from ..models import Admin
from ..schemas.AdminSchema import AdminSchema
from ..functions.Methods import pagination

admin_schema = AdminSchema()

@api.route('/admin/add', methods=['POST'])
@jwt_required
@admin_required
def add_admin():
    json_data = request.get_json()
    try:
        admin_data = admin_schema.load(json_data)
    except ValidationError as error:
        return error.messages, 400
    admin = Admin.username_exists(json_data['username'])
    if admin:
        return {"msg": "User already exists try diffrent username."}
    admin = Admin(**json_data)
    try:
        admin.save_data()
    except IntegrityError as error:
        admin.session.rollback()
        return error._message(IndentationError), 500
    confirm_code = admin.generate_confirm_number(current_app.config['SECRET_KEY'], expiration=1800)
    send_verfy_mail(json_data['email'], current_app.config['UST_MAIL'], confirm_code, json_data['password'])
    return {
        "msg": "Admin added correctly.",
        "new admin": admin_schema.dump(admin)
    }, 200

@api.route('/admin/<string:username>', methods=['GET'])
@jwt_required
@admin_required
def get_admin(username):
    try:
        admin = Admin.find_by_username(username)
    except IntegrityError as error:
        return error._message()
    if not admin:
        return {"msg": "not found"}, 404
    admin_data = admin_schema.dump(admin)
    return {"data:": admin_data}

@api.route('/admin/edit/<int:id>', methods=['PUT'])
@jwt_required
@admin_required
def edit_admin(id):
    json_data = request.get_json()
    try:
        admin = Admin.find_by_id(id)
    except IntegrityError as error:
        return error._message()
    if not admin:
        return {"msg": "not found"}, 404
    try:
        admin_data = admin_schema.dump(admin)
    except ValidationError as error:
        return error.messages, 400
    try:
        if 'email' in json_data:
            if Admin.query.filter_by(email=json_data['email']).first():
                return {"msg": "email already exists"}, 500
            admin.email = json_data['email']

        if 'phone' in json_data:
            if Admin.find_by_phone(json_data['phone']):
                return {"msg": "phone already exists"}, 500
            admin.phone = json_data['phone']

        if 'username' in json_data:
            if Admin.find_by_username(json_data['username']):
                return {"msg": "username already token"}
            admin.username = json_data['username']
        
        if 'admin_card' in json_data:
            if Admin.query.filter_by(admin_card=json_data['admin_card']).first():
                return {"msg": "admin card number can't be depreceted."}
            admin.admin_card = json_data['admin_card']
        
        if 'surename' in json_data:
            admin.surename = json_data['surename']
        if 'gendre' in json_data:
            admin.gendre = json_data['gendre']
        if 'password' in json_data:
            return {"msg": "unautherized action, only the account user can edit his password"}
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    try:
        admin = Admin.find_by_id(id)
        admin_data = admin_schema.dump(admin)
    except ValidationError as error:
        return error.messages, 400
    return {"msg": "data has been updated.", "data": dept_data}

@api.route('/admin/delete/<string:username>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_admin(username):
    try:
        admin = Admin.find_by_username(username)
    except IntegrityError as error:
        return error._message()
    if not admin:
        return {"msg": "not found"}, 404
    try:
        admin.delete_data()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    return {"msg": "admin data has been deleted."}

@api.route('/admin/all', methods=['GET'])
def get_admins():
    pass