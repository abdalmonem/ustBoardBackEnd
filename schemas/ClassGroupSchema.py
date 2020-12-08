from marshmallow import fields
from configurations import ma

class ClassGroupSchema(ma.Schema):
    title = fields.Str()
    year = fields.Int()
    c_type = fields.Int()
    dept = fields.Int()

