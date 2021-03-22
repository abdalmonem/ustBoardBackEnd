from marshmallow import fields
from .UserSchema import UserSchema
from .. import ma

class SupervisorSchema(UserSchema):
    super_card = fields.Str()
    dept_id = fields.Int()
