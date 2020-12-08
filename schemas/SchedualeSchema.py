from marshmallow import fields
from configurations import ma

class SchedualeSchema(ma.Schema):
    year = fields.Int()
    position = fields.Int()
    day = fields.Str()
    material_id = fields.Int()
    teacher_id = fields.Int()