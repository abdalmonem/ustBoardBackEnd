from marshmallow import fields
from .. import ma

class MaterialSchema(ma.Schema):
    title = fields.Str()
    h_rate = fields.Int()
    dept_id = fields.Int()
