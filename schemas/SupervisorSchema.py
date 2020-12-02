from marshmallow import fields
from schemas.UserSchema import UserSchema

class SupervisorSchema(UserSchema):
    user_id = fields.Int()