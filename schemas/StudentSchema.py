# from configurations import ma
from marshmallow import fields
from schemas.UserSchema import UserSchema

class StudentSchema(UserSchema):
    user_id = fields.Int()
    year = fields.Int()
    card_id = fields.Str()
    # surename = fields.Str()