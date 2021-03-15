from .. import db

class DeptModel(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    year = db.Column(db.Integer, nullable=False)
    dept_type = db.Column(db.String(50), nullable=False)
    students = db.relationship('Student', backref='partition')
    supervisor = db.relationship('Supervisor', backref='supervisation', uselist=False)
    materials = db.relationship('Materials', backref='dept_materials')
    d_lab_group = db.relationship('LabGroup', backref='lab_group_depts')
    d_class_group = db.relationship('ClassGroup', backref='class_group_depts')

    def __init__(self, **kwargs):
        super(DeptModel, self).__init__(**kwargs)

    @classmethod
    def check_dept(cls, title, dept_type):
        return cls.query.filter_by(title=title, dept_type=dept_type).first()
    
    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_data(self):
        db.session.add(self)
        db.session.commit()

    def delete_data(self):
        db.session.delete(self)
        db.session.commit()