from marshmallow import fields
from configurations import db
from .SchedualeSchema import SchedualeSchema

class ClassSchedualSchema(SchedualeSchema):
    class_id = fields.Int()