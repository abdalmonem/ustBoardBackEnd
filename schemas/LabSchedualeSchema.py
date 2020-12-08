from marshmallow import fields
from configurations import db
from .SchedualeSchema import SchedualeSchema

class LabSchedualSchema(SchedualeSchema):
    lab_id = fields.Int()