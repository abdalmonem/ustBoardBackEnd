from flask import request
from configurations import jwt
from flask_restful import Resource
from models.UsersModel import Users
from schemas.UserSchema import UserSchema
from marshmallow import ValidationError
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_claims,
    get_jwt_identity
)

user_schema = UserSchema()

class Login(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            data = user_schema.load(json_data)
        except ValidationError as error:
            return error.messages
        user = Users.find_by_phone(data['phone'])
        if user and user.password_check(data['password']):
            access_token = create_access_token(identity=user.rank, fresh=True)
            return { "TOKEN": access_token, "id": user.id, "rank": user.rank }, 200
        else:
            return { "error": "Either User not found or Invalid request \"input\"." }, 400


class Logout(Resource):
    pass

