from marshmallow import fields
from .. import ma

class SchedualeSchema(ma.Schema):
    position = fields.Int()
    day = fields.Str()
    material_id = fields.Int()
