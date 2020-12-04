from marshmallow import fields
from schemas.StudentSchema import UserSchema

class AdminSchema(UserSchema):
    user_id = fields.Int()

