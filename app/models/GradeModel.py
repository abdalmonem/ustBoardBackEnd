from .. import db

class Grades(db.Model):
    __tablename__ = 'grades_table'
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    grade = db.Column(db.String(2), nullable=False)
    std = db.Column(db.Integer, db.ForeignKey('students.id'))
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'))

    def __init__(self, **kwargs):
        super(Grades, self).__init__(**kwargs)
