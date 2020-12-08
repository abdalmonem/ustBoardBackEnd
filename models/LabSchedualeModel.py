from configurations import db
from models.SchedualeModel import SchedualeModel

class LabSchedualeModel(SchedualeModel):
    __tablename__ = 'lab_scheduales'
    id = db.Column(db.Integer, db.ForeignKey('schedules.id'), primary_key=True)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab_group.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'lab_scheduales',
    }

    def __init__(self, year, position, day, material_id, teacher_id, lab_id):
        super().__init__(year, position, day, material_id, teacher_id)
        self.lab_id = lab_id

