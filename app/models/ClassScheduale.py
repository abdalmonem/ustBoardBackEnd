from .. import db
from .SchedualeModel import SchedualeCells

class ClassSchedualeCells(SchedualeCells):
    __tablename__ = 'class_scheduale'
    id = db.Column(db.Integer, db.ForeignKey('schedules.id'), primary_key=True)
    time = db.Column(db.String(10))
    class_id = db.Column(db.Integer, db.ForeignKey('class_group.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'class'
