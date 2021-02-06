from marshmallow import fields
from .UserSchema import UserSchema

class TeacherSchema(UserSchema):
    teacher_card_id = fields.Str()
