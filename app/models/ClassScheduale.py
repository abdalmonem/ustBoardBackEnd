from .. import db
from .SchedualeModel import SchedualeCells

class ClassSchedualeCells(SchedualeCells):
    __tablename__ = 'class_scheduale'
    id = db.Column(db.Integer, db.ForeignKey('schedules.id'), primary_key=True)
    time = db.Column(db.String(10))
    class_id = db.Column(db.Integer, db.ForeignKey('class_group.id'))

    def __init__(self, time, class_id, **kwargs):
        super().__init__(**kwargs)
        self.time = time
        self.class_id = class_id
        self.type = 'class'
