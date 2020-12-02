from configurations import db
from models.UsersModel import Users

class Admin(Users):
    _tabelname_ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship(Users)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))

    def __init__(self, username, password, email, phone, surename, date, user_id):
        super().__init__(username, password, email, phone, surename, date)
        self.user_id = user_id
        self.rank = 2
