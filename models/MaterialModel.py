from configurations import db


class Materials(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    h_rate = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    dept = db.relationship('DeptModel')
    teachers = db.relationship('Teachers')
    # grade = db.relationship('GradeScheduale', uselist=False)

    def __init__(self, title, h_rate, year, dept_id):
        self.title = title
        self.h_rate = h_rate
        self.year = year
        self.dept_id = dept_id

    @classmethod
    def check_material(cls, title):
        return cls.query.filter_by(title=title).first()

    def save_data(self):
        db.session.add(self)
        db.session.commit()

    def get_title(self):
        return self.title

