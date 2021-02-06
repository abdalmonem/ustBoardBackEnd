from marshmallow import fields
from .SchedualeSchema import SchedualeSchema

class LabSchedualSchema(SchedualeSchema):
    time = fields.Str()
    lab_id = fields.Int()
