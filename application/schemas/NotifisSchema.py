from marshmallow import fields
from .. import ma

class NotificationSchema(ma.Schema):
    title = fields.Str()
    position = fields.Int()
    date = fields.Str()
    content = fields.Str()
    std_id = fields.Int()
    teacher_id = fields.Int()
    supervisor = fields.Int()
