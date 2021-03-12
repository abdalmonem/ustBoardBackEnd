# from configurations import ma
from marshmallow import fields
from .UserSchema import UserSchema

class StudentSchema(UserSchema):
    year = fields.Int()
    card_id = fields.Str()
