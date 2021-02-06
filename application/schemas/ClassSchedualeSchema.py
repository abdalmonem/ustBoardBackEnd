from marshmallow import fields
from .SchedualeSchema import SchedualeSchema

class ClassSchedualSchema(SchedualeSchema):
    time = fields.Str()
    class_id = fields.Int()
