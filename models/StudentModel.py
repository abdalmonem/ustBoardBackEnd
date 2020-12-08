from configurations import db
from models.UsersModel import Users

class Student(Users):
    __tablename__ = 'students'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    card_id = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __init__(self, username, password, email, phone, surename, date, year, card_id, dept_id):
        super().__init__(username, password, email, phone, surename, date)
        self.rank = 0
        self.name = surename
        self.year = year
        self.card_id = card_id
        self.dept_id = dept_id

