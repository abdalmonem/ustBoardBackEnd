from marshmallow import fields
from schemas.UserSchema import UserSchema

class SupervisorSchema(UserSchema):
    super_card_id = fields.Str()
    dept_id = fields.Int()