from marshmallow import fields
from .UserSchema import UserSchema
from .. import ma

class SupervisorSchema(UserSchema):
    super_card = fields.Str()


# class SupervisorQueries(SupervisorSchema):
#     page_num = fields.Int()
#     amount = fields.Int()
