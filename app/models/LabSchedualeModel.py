from .. import db
from .SchedualeModel import SchedualeCells

class LabSchedualeCells(SchedualeCells):
    __tablename__ = 'lab_scheduales'
    id = db.Column(db.Integer, db.ForeignKey('schedules.id'), primary_key=True)
    time = db.Column(db.String(10))
    lab_id = db.Column(db.Integer, db.ForeignKey('lab_group.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'lab'
