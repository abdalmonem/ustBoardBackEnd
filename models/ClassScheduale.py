from configurations import db
from models.SchedualeModel import SchedualeModel
from models.ClassGroupModel import ClassGroupModel

class ClassSchedualeModel(SchedualeModel):
    __tablename__ = 'class_scheduale'
    id = db.Column(db.Integer, db.ForeignKey('schedules.id'), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class_group.id'))
    # class_group = db.relationship('ClassGroupModel')

    __mapper_args__ = {
        'polymorphic_identity': 'class_scheduale',
    }

    def __init__(self, year, position, day, material_id, teacher_id, class_id):
        super().__init__(year, position, day, material_id, teacher_id)
        self.class_id = class_id

