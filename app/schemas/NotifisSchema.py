from marshmallow import fields
from .. import ma

class NotificationSchema(ma.Schema):
    title = fields.Str()
    date = fields.Str()
    content = fields.Str()
    student_id = fields.Int()
    teacher_id = fields.Int()
    class_id = fields.Int()
    lab_id = fields.Int()
