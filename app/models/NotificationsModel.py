from .. import db
from datetime import datetime

class Notifications(db.Model):
    __tabelname__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    # target = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class_group.id'), nullable=True)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab_group.id'), nullable=True)

    def __init__(self, title, content, student_id=0, teacher_id=0, class_id=0, lab_id=0):
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.class_id = class_id
        self.lab_id = lab_id
        self.title = title
        self.content = content

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
