from marshmallow import fields
from .. import ma

class GradeSchema(ma.Schema):
    position = fields.Int()
    grade = fields.Str()
    std = fields.Int()
    material = fields.Int()
    class_group = fields.Int()
