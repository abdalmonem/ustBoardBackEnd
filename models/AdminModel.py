from configurations import db
from models.UsersModel import Users

class Admin(Users):
    _tabelname_ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    user: Users = db.relationship(Users)
    admin_name = db.Column(db.String(255), nullable=False)
    adimn_id = db.Column(db.Integer, db.ForeignKey(Users.id))

    def __init__(self, username, password, email, phone, surename, date):
        super().__init__(username, password, email, phone, surename, date)
        self.rank = 2
        self.admin_name = surename
