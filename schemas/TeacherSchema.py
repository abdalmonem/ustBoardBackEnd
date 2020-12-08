from marshmallow import fields
from schemas.UserSchema import UserSchema

class TeacherSchema(UserSchema):
    teacher_card_id = fields.Str()
    dept_id = fields.Int()
    material_id = fields.Int()

