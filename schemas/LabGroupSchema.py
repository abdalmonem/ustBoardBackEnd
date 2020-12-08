from marshmallow import fields
from configurations import ma

class LabGroupSchema(ma.Schema):
    title = fields.Str()
    year = fields.Int()
    g_type = fields.Int()
    dept = fields.Int()

