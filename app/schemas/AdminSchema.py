from marshmallow import fields
from .UserSchema import UserSchema

class AdminSchema(UserSchema):
    admin_card = fields.Str()

