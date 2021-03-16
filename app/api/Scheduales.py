from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required
from . import api
from .. import db
from .decorators import supervisor_required
from ..models import SchedualeCells, ClassSchedualeCells, LabSchedualeCells, ClassGroup, LabGroup
from ..schemas.LabSchedualeSchema import LabSchedualSchema
from ..schemas.ClassSchedualeSchema import ClassSchedualSchema

class_schud_schema = ClassSchedualSchema()
lab_schud_schema = LabSchedualSchema()

@api.route('/class-scheduale/add', methods=['POST'])
@jwt_required
@supervisor_required
def add_class_schedual():
    json_data = request.get_json()
    try:
        class_data = class_schud_schema.load(json_data)
    except ValidationError as error:
        return error.messages
    data = ClassSchedualeCells(**class_data)
    try:
        data.save_data()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(IndentationError)
    return class_schud_schema.dump(data)

@api.route('/lab-scheduale/add', methods=['POST'])
@jwt_required
@supervisor_required
def add_lab_scheduale():
    json_data = request.get_json()
    try:
        lab_data = lab_schud_schema.load(json_data)
    except ValidationError as error:
        return error.messages
    data = LabSchedualeCells(**lab_data)
    try:
        data.save_data()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(IndentationError)
    return lab_schud_schema.dump(data) 

@api.route('/class-scheduale/<int:class_id>', methods=['GET'])
@jwt_required
@supervisor_required
def get_class_scheduale(class_id):
    try:
        class_group = ClassGroup.find_by_id(class_id)
    except IntegrityError as error:
        return error._message()
    if not class_group:
        return {"msg": "not found"}, 404
    class_cells = class_group.class_scheduale.order_by(ClassSchedualeCells.position.desc())
    if not class_group:
        return {"msg": "class group not found."}
    cells_data = class_schud_schema.dump(class_cells, many=True)
    return {"data:": cells_data}

@api.route('/lab-scheduale/<int:id>', methods=['GET'])
@jwt_required
@supervisor_required
def get_lab_scheduale(id):
    try:
        lab_group = LabGroup.find_by_id(class_id)
    except IntegrityError as error:
        return error._message()
    if not lab_group:
        return {"msg": "not found"}, 404
    lab_cells = lab_group.class_scheduale.order_by(LabSchedualeCells.position.desc())
    if not class_group:
        return {"msg": "class group not found."}
    cells_data = lab_schud_schema.dump(lab_cells, many=True)
    return {"data:": cells_data}

@api.route('/class-scheduale/edit/<int:id>', methods=['PUT'])
@jwt_required
@supervisor_required
def edit_class_scheduale(id):
    json_data = request.get_json()
    try:
        class_sched = ClassSchedualeCells.find_by_id(id)
    except IntegrityError as error:
        return error._message()
    if not class_sched:
        return {"msg": "not found"}, 404
    try:
        if 'class_id' in json_data:
            class_sched.class_id = json_data['class_id']
        if 'day' in json_data:
            class_sched.day = json_data['day']
        if 'position' in json_data:
            class_sched.position = json_data['position']
        if 'time' in json_data:
            class_sched.time = json_data['time']
        if 'material_id' in json_data:
            class_sched.material_id = json_data['material_id']
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    try:
        class_sched = ClassSchedualeCells.find_by_id(id)
        cell_data = class_schud_schema.dump(class_sched)
    except ValidationError as error:
        return error.messages, 400
    return {"msg": "data has been updated.", "data": cell_data}

@api.route('/lab-scheduale/edit/<int:id>', methods=['PUT'])
@jwt_required
@supervisor_required
def edit_lab_scheduale(id):
    json_data = request.get_json()
    try:
        lab_sched = LabSchedualeCells.find_by_id(id)
    except IntegrityError as error:
        return error._message()
    if not lab_sched:
        return {"msg": "not found"}, 404
    try:
        if 'class_id' in json_data:
            lab_sched.class_id = json_data['class_id']
        if 'day' in json_data:
            lab_sched.day = json_data['day']
        if 'position' in json_data:
            lab_sched.position = json_data['position']
        if 'time' in json_data:
            lab_sched.time = json_data['time']
        if 'material_id' in json_data:
            lab_sched.material_id = json_data['material_id']
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    try:
        lab_sched = LabSchedualeCells.find_by_id(id)
        cell_data = lab_schud_schema.dump(lab_sched)
    except ValidationError as error:
        return error.messages, 400
    return {"msg": "data has been updated.", "data": cell_data}

@api.route('/class-scheduale/delete/<int:id>', methods=['Delete'])
@jwt_required
@supervisor_required
def delete_class_scheduale(id):
    try:
        class_sched = ClassSchedualeCells.find_by_id(id)
    except IntegrityError as error:
        return error._message()
    if not class_sched:
        return {"msg": "not found"}, 404
    try:
        class_sched.delete_data()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    return {"msg": "data has been deleted."}

@api.route('/lab-scheduale/delete/<int:id>', methods=['Delete'])
@jwt_required
@supervisor_required
def delete_lab_scheduale(id):
    try:
        lab_sched = LabSchedualeCells.find_by_id(id)
    except IntegrityError as error:
        return error._message()
    if not lab_sched:
        return {"msg": "not found"}, 404
    try:
        lab_sched.delete_data()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    return {"msg": "data has been deleted."}
