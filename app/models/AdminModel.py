from .. import db
from .UsersModel import Users

class Admin(Users):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    admin_card = db.Column(db.String(20), nullable=True)

    def __init__(self, admin_card, **kwargs):
        super().__init__(**kwargs)
        self.admin_card = admin_card
        self.rank = 3
        self.username = admin_card
        self.type = 'admin'
