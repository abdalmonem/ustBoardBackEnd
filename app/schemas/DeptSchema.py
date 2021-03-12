from marshmallow import fields
from .. import ma

class DeptSchema(ma.Schema):
    title = fields.Str()
    year = fields.Int()
    dept_type = fields.Str()
