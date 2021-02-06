from flask import request, jsonify
# from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update
from .decorators import admin_required
from . import api
from ..models import Supervisor
from ..schemas.AdminSchema import AdminSchema
from ..functions.Methods import pagination

@api.route('/admin/add', methods=['POST'])
def add_admin():
    pass

@api.route('/admin/<string:username>', methods=['GET'])
def get_admin(username):
    pass

@api.route('/admin/edit/<string:username>', methods=['POST'])
def edit_admin(username):
    pass

@api.route('/admin/delete/<string:username>', methods=['DELETE'])
def delete_admin(username):
    pass

@api.route('/admin/all', methods=['GET'])
def get_admins():
    pass
