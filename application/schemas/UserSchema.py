from marshmallow import fields
from .. import ma

class UserSchema(ma.Schema):
    class Meta:
        load_only = ('date', 'admin_card')
        dump_only = ('id',)
    # id = fields.Int()
    username = fields.Str()
    password = fields.Str()
    email = fields.Str()
    phone = fields.Str()
    surename = fields.Str()
    gendre = fields.Int()
