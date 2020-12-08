from configurations import db
from models.UsersModel import Users

class Admin(Users):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    admin_name = db.Column(db.String(150), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __init__(self, username, password, email, phone, surename, date):
        super().__init__(username, password, email, phone, surename, date)
        self.rank = 3
        self.admin_name = surename

