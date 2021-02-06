from .. import db

class SchedualeCells(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    day = db.Column(db.String(5), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'))
    type = db.Column(db.String(50))

    def __init__(self, **kwargs):
        super(SchedualeCells, self).__init__(**kwargs)

    def save_data(self):
        db.session.add(self)
        db.session.commit()
