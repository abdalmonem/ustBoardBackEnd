from .. import db

class LabGroup(db.Model):
    __tablename__ = 'lab_group'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.Integer, unique=True)
    center_number = db.Column(db.Integer)
    lab_number = db.Column(db.Integer)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    lab_cells = db.relationship('LabSchedualeCells', backref='lab_schedual_cells')
    lab_group_noti = db.relationship('Notifications', backref='lab_group_alerts')

    def __init__(self, **kwargs):
        super(LabGroup, self).__init__(**kwargs)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(group_name=name).first()
    
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
