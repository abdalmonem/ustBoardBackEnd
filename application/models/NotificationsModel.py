from .. import db

class Notifications(db.Model):
    __tabelname__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date)
    content = db.Column(db.Text, nullable=False)
    target = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class_group.id'), nullable=True)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab_group.id'), nullable=True)

    def __init__(self, **kwargs):
        super(Notifications, self).__init__(**kwargs)
