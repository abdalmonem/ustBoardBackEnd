from configurations import db

class LabGroupModel(db.Model):
    __tablename__ = 'lab_group'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    g_type = db.Column(db.Integer)
    dept = db.Column(db.Integer, db.ForeignKey('departments.id'))
    scheduals = db.relationship('LabSchedualeModel', lazy='dynamic')

    def __init__(self, title, year, g_type, dept):
        self.title = title
        self.year = year
        self.g_type = g_type
        self.dept_id = dept

    def save_data(self):
        db.session.add(self)
        db.session.commit()

