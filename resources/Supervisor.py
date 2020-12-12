from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from models.SuperVisorModel import Supervisor
from schemas.SupervisorSchema import SupervisorSchema
from flask_jwt_extended import jwt_required

supervisor_schema = SupervisorSchema()

class SuperVisor(Resource):
    @jwt_required
    def post(self):
        json_data = request.get_json()
        try:
            data = supervisor_schema.load(json_data)
        except ValidationError as error:
            return error.messages
        supervisor = Supervisor.find_by_phone(data['phone'])
        if supervisor:
            return {"message": "Supervisor already exists."}
        supervisor = Supervisor(**data)
        try:
            supervisor.save_data()
        except IntegrityError as error:
            return error._message(IndentationError)
        return supervisor_schema.dump(supervisor)

    @jwt_required
    def get(self, card_id):
        supervisor = Supervisor.find_by_card_id(card_id)
        if supervisor:
            return supervisor_schema.dump(supervisor)
        return {"msg": "User not found."}, 404

    @jwt_required
    def put(self, name):
        json_data = request.get_json()
        supervisor = Supervisor.find_by_username(name)
        if supervisor:
            pass
        return {"msg": "User not found."}, 404


