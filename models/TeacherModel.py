from configurations import db
from models.UsersModel import Users
from models.DeptModel import DeptModel

class Teachers(Users):
    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.String(80), nullable=False)
    user: Users = db.relationship(Users)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    dept: DeptModel = db.relationship(DeptModel)
    dept_id = db.Column(db.Integer, db.ForeignKey(DeptModel.id))

    def __init__(self, username, password, email, phone, surename, date, teacher_id, dept_id, material_id):
        super().__init__(username, password, email, phone, surename, date)
        self.teacher_name = surename
        self.teacher_id = teacher_id
        self.dept_id = dept_id
        self.material_id = material_id

