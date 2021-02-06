from marshmallow import fields
from .. import ma

class ClassGroupSchema(ma.Schema):
    group_name = fields.Str()
    hall_number = fields.Int()
    scheduale = fields.Int()
    dept = fields.Int()
