from configurations import db
from models.DeptModel import DeptModel
from models.TeacherModel import Teachers

class Materials(db.Model):
    _tabelname_ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    h_rate = db.Column(db.Interger, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    teacher: Teachers = db.relationship(Teachers)
    teacher_id = db.Column(db.Integer, db.ForeignKey(Teachers.id))
    dept: DeptModel = db.relationship(DeptModel)
    dept_id = db.Column(db.Integer, db.ForeignKey(DeptModel.id))

    def __init__(self, title, h_rate, year, teacher_id, dept_id):
        self.title = title
        self.h_rate = h_rate
        self.year = year
        self.teacher_id = teacher_id
        self.dept_id = dept_id

