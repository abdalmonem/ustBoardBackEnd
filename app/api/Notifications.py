from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import api
from .. import db
from .decorators import supervisor_required
from ..models import Notifications
from ..schemas import NotificationSchema

notifi_schema = NotificationSchema()

@api.route('/notification/send', methods=['POST'])
@jwt_required
@supervisor_required
def send_notification():
	json_data = request.get_json()
	if request.method == 'POST':
		try:
			notifi_data = notifi_schema.load(json_data)
		except ValidationError as error:
			return error.messages, 400
		notifi_obj = Notifications(**json_data)
		try:
			notifi_obj.save_data()
		except IntegrityError as error:
			return error._message(), 500
		return notifi_schema.dump(notifi_obj)
	return {"msg": "invalid link"}, 400

@api.route('/notification/edit/<int:id>', methods=['GET'])
@jwt_required
@supervisor_required
def show_notification(id):
	if request.method == 'GET':
		try:
            notifi_obj = Notifications.find_by_id(id)
        except IntegrityError as error:
            return error._message()
        if not notifi_obj:
            return {"msg": "not found"}, 404
        try:
            notifi_data = notifi_schema.dump(notifi_obj)
        except ValidationError as error:
            return error.messages, 400
        try:
            if 'title' in json_data:
                notifi_obj.title = json_data['title']
            if 'content' in json_data:
                notifi_obj.h_rate = json_data['content']
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            return error._message(), 500
        try:
            notifi_obj = Materials.find_by_id(id)
            notifi_data = notifi_schema.dump(notifi_obj)
        except ValidationError as error:
            return error.messages, 400
        return {"msg": "data has been updated.", "data": notifi_data}
	return {"msg": "invalid link"}, 400

@api.route('/notification/delete/<int:id>', methods=['DELETE'])
@jwt_required
@supervisor_required
def delete_notification(id):
	if request.method == 'DELETE':
		try:
			notifi_obj = Notifications.find_by_id(id)
		except IntegrityError as error:
			return error._message(), 500
		if not notifi_obj:
			return {"msg": "not found"}, 404
		try:
			notifi_obj.delete_data()
		except IntegrityError as error:
			db.session.rollback()
			return error._message(), 500
		return {"msg": "data has been deleted"}, 200
	return {"msg": "invalid link"}, 400
