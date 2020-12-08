from configurations import db

class DeptModel(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    year = db.Column(db.Integer, nullable=False)
    dept_type = db.Column(db.String(50), nullable=False)
    student = db.relationship('Student', uselist=False)
    supervisor = db.relationship('Supervisor', uselist=False)
    materials = db.relationship('Materials')
    class_group = db.relationship('ClassGroupModel', uselist=False)
    lab_group = db.relationship('LabGroupModel', uselist=False)

    __mapper_args__ = { 
        'polymorphic_identity': 'department'
    }

    def __init__(self, title, year, dept_type):
        self.title = title
        self.year = year
        self.dept_type = dept_type

    @classmethod
    def check_dept(cls, title):
        return cls.query.filter_by(title=title).first()

    def save_data(self):
        db.session.add(self)
        db.session.commit()

    def get_title(self):
        return self.title

    def get_type(self):
        return self.dept_type

