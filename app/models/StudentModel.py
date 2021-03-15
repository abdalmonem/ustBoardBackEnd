from .. import db
from .UsersModel import Users

class Student(Users):
    __tablename__ = 'students'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    card_id = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(20), nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    grades = db.relationship('Grades', backref='material_grades')
    student_noti = db.relationship('Notifications', backref='student_alerts')

    def __init__(self, card_id, year, **kwargs):
        super().__init__(**kwargs)
        self.card_id = card_id
        self.type = 'students'
        self.year = year

    def get_rank(self):
        return self.rank
        self.type = 'student'
