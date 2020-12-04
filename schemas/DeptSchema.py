from configurations import ma
from marshmallow import fields

class DeptSchema(ma.Schema):
    title = fields.Str()
    year = fields.Int()
    dept_type = fields.Str()

