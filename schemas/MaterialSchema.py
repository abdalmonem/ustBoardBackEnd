from configurations import ma
from marshmallow import fields

class MaterialSchema(ma.Schema):
    title = fields.Str()
    h_rate = fields.Int()
    year = fields.Int()
    dept_id = fields.Int()