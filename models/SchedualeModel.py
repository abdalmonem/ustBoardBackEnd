from configurations import db

class SchedualeModel(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer)
    day = db.Column(db.String(5), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'))
    material = db.relationship('Materials')
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    material = db.relationship('Teachers')
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'schedules',
        'polymorphic_on': type
    }

    def __init__(self, year, position, day, material_id, teacher_id):
        self.year = year
        self.position = position
        self.day = day
        self.material_id = material_id
        self.teacher_id = teacher_id

    def save_data(self):
        db.session.add(self)
        db.session.commit()

