from marshmallow import fields
from .. import ma

class LabGroupSchema(ma.Schema):
    group_name = fields.Str()
    center_number = fields.Int()
    lab_number = fields.Int()
    dept = fields.Int()
