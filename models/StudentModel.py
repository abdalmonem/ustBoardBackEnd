from configurations import db
from models.UsersModel import Users

class Student(Users):
    _tabelname_ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    card_id = db.Column(db.String(100), nullable=False)
    user: Users = db.relationship(Users)
    year = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey(Users.id))

    def __init__(self, username, password, email, phone, surename, date, year, card_id):
        super().__init__(username, password, email, phone, surename, date)
        self.year = year
        self.card_id = card_id
        self.rank = 0
        self.name = surename

