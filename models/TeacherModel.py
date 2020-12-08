from configurations import db
from models.UsersModel import Users
# from sqlalchemy import Table, Column, ForeignKey

class Teachers(Users):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    teacher_name = db.Column(db.String(100), nullable=False)
    teacher_card_id = db.Column(db.String(80), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'))
    material = dept = db.relationship('Materials')
    __mapper_args__ = {
        'polymorphic_identity': 'teachers',
    }

    def __init__(self, username, password, email, phone, surename, date, teacher_card_id, material_id, dept_id):
        super().__init__(username, password, email, phone, surename, date)
        self.teacher_name = surename
        self.rank = 2
        self.teacher_card_id = teacher_card_id
        self.material_id = material_id
        self.dept_id = dept_id 

