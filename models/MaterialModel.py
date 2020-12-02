from configurations import db
from models.DeptModel import DeptModel

class Materials(db.Model):
    _tabelname_ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    h_rate = db.Column(db.Interger, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    dept: DeptModel = db.relationship(DeptModel)
    dept_id = db.Column(db.Integer, db.ForeignKey(DeptModel.id))

    def __init__(self, title, h_rate, year):
        self.title = title
        self.h_rate = h_rate
        self.year = year
        self.dept_id = self.dept.id

