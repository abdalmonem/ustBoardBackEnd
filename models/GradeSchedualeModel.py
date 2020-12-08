from configurations import db

class GradeScheduale(db.Model):
    __tablename__ = 'grade_scheduale'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'))
    material = db.relationship('Materials')
    grade = db.Column(db.String(2))
    material = db.relationship('Teachers')
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    def __init__(self, year, position, material_id, grade, dept_id):
        self.year = year
        self. position = position
        self.material_id = material_id
        self.grade = grade
        self. dept_id = dept_id

    def save_data(self):
        db.session.add(self)
        db.session.commit()