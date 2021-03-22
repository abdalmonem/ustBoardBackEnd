from .. import db
from .UsersModel import Users

class Supervisor(Users):
    __tablename__ = 'supervisor'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    super_card = db.Column(db.String(80), nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    def __init__(self, super_card, dept_id, **kwargs):
        super().__init__(**kwargs)
        self.super_card = super_card
        self.rank = 2
        self.dept_id = dept_id
        self.type = 'supervisor'
        self.confirmed = False

    @classmethod
    def find_by_card_id(cls, super_card_id):
        return cls.query.filter_by(super_card_id=super_card_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.with_entities(cls.surename, cls.dept_id).all()
