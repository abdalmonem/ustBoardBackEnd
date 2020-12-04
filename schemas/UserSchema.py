from configurations import ma
from marshmallow import fields

class UserSchema(ma.Schema):
    class Meta:
        load_only = ('password',)
    username = fields.Str()
    password = fields.Str()
    email = fields.Str()
    phone = fields.Str()
    surename = fields.Str()
    date = fields.Int()

