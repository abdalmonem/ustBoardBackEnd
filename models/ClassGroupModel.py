from configurations import db

class ClassGroupModel(db.Model):
    __tablename__ = 'class_group'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    c_type = db.Column(db.Integer)
    dept = db.Column(db.Integer, db.ForeignKey('departments.id'))
    scheduales = db.relationship('ClassSchedualeModel', lazy='dynamic')
    
    def __init__(self, title, year, c_type, dept):
        self.title = title
        self.year = year
        self.g_type = c_type
        self.dept_id = dept

    def save_data(self):
        db.session.add(self)
        db.session.commit()

