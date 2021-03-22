from .. import db
from .UsersModel import Users

class Teachers(Users):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    teacher_card = db.Column(db.String(80), nullable=False)
    teachers = db.relationship('Materials', backref='materials')
    teacher_noti = db.relationship('Notifications', backref='teacher_alerts')

    def __init__(self, teacher_card, **kwargs):
        super().__init__(**kwargs)
        self.teacher_card = teacher_card
        self.rank = 1
        self.type = 'teacher'
