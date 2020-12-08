from configurations import db
from models.UsersModel import Users
# from models.DeptModel import DeptModel

class Supervisor(Users):
    __tablename__ = 'supervisor'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    super_card_id = db.Column(db.String(80), nullable=False)
    super_name = db.Column(db.String(100))
    dept = db.relationship('DeptModel')
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'supervisor',
    }

    def __init__(self, username, password, email, phone, surename, date, super_card_id, dept_id):
        super().__init__(username, password, email, phone, surename, date)
        self.super_card_id = super_card_id
        self.dept_id = dept_id
        self.rank = 1
        self.super_name = surename

    @classmethod
    def find_by_card_id(cls, super_card_id):
        return cls.query.filter_by(super_card_id=super_card_id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

