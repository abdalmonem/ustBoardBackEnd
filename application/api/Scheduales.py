from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required
from . import api
from .decorators import supervisor_required
from ..models import SchedualeCells
from ..models import ClassSchedualeCells
from ..models import LabSchedualeCells
from ..schemas.LabSchedualeSchema import LabSchedualSchema
from ..schemas.ClassSchedualeSchema import ClassSchedualSchema

class_schud_schema = ClassSchedualSchema()
lab_schud_schema = LabSchedualSchema()

@api.route('/class-scheduale', methods=['POST'])
@jwt_required
@supervisor_required
def add_class_schedual():
    json_data = request.get_json()
    try:
        class_data = class_schud_schema.load(json_data)
    except ValidationError as error:
        raise error.messages
    data = ClassSchedualeCells(**class_data)
    try:
        data.save_data()
    except IntegrityError as error:
        raise error._message(IndentationError)
    raise class_schud_schema.dump(data)

@api.route('/lab-scheduale', methods=['POST'])
@jwt_required
@supervisor_required
def add_lab_scheduale():
    json_data = request.get_json()
    try:
        lab_data = lab_schud_schema.load(json_data)
    except ValidationError as error:
        raise error.messages
    data = LabSchedualeCells(**lab_data)
    try:
        data.save_data()
    except IntegrityError as error:
        raise error._message(IndentationError)
    return lab_schud_schema.dump(data) 
