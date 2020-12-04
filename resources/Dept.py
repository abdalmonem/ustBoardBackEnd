from flask import request
from flask_restful import Resource
from models.DeptModel import DeptModel
from schemas.DeptSchema import DeptSchema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required


dept_schema = DeptSchema()

class AddDept(Resource):
    @jwt_required
    def post(self):
        json_data = request.get_json()
        try:
            dept_data = dept_schema.load(json_data)
        except ValidationError as error:
            return error.messages
        dept = DeptModel.check_dept(dept_data['title'])
        if dept:
            return {"message": "Dept already exists."}
        dept = DeptModel(**json_data)
        try:
            dept.save_data()
        except IntegrityError as error:
            return error._message(IndentationError)
        return dept_schema.dump(dept)

