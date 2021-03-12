from .. import db

class ClassGroup(db.Model):
    __tablename__ = 'class_group'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100), nullable=False)
    hall_number = db.Column(db.Integer, unique=True)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    # class_group_depts = db.relationship('DeptModel', back_populates='d_class_group')
    class_group_noti = db.relationship('Notifications', backref='class_group_alerts')
    class_scheduale = db.relationship('ClassSchedualeCells', backref='class_schedual_cells')
    
    def __init__(self, **kwargs):
        super(ClassGroup, self).__init__(**kwargs)
