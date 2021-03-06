from .. import db

class Materials(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    h_rate = db.Column(db.Integer, nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    grades = db.relationship('Grades', backref='final_grade', uselist=False)
    cells = db.relationship('SchedualeCells', backref='cell')

    def __init__(self, **kwargs):
        super(Materials, self).__init__(**kwargs)

    @classmethod
    def check_material(cls, title, dept_id):
        if cls.query.filter_by(title=title, dept_id=dept_id).first():
            return True
        return False
    
    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_row_count(cls):
        return cls.query.count()

    def save_data(self):
        db.session.add(self)
        db.session.commit()

    def delete_data(self):
        db.session.delete(self)
        db.session.commit()

