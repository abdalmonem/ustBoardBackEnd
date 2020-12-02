from configurations import db
from models.UsersModel import Users
from models.DeptModel import DeptModel

class Supervisor(Users):
    _tabelname_ = 'supervisor'
    id = db.Column(db.Integer, primary_key=True)
    super_card_id = db.Column(db.String(100), nullable=False)
    user: Users = db.relationship(Users)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    dept: DeptModel = db.relationship(DeptModel, uselist=False)
    dept_name = db.Column(db.String(100), nullable=False)
    dept_type = db.Column(db.String(50), nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey(DeptModel.id))

    def __init__(self, username, password, email, phone, surename, date, super_card_id, dept_id):
        super().__init__(username, password, email, phone, surename, date)
        self.super_card_id = super_card_id
        self.dept_id = dept_id
        self.rank = 1
        self.dept_name = self.dept.title
        self.dept_type = self.dept.dept_type

