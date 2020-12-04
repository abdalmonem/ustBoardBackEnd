from configurations import db
from models.SupervisorModel import Supervisor

class ClassGroupModel(db.Model):
    _tabelname_ = 'class_group'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    c_type = db.Column(db.Integer)
    supervisor: Supervisor = db.relationship(Supervisor)
    supervisor_id = db.Column(db.Integer, db.ForeignKey(Supervisor.id))
    
    def __init__(self, title, year, c_type, supervisor_id):
        self.title = title
        self.year = year
        self.g_type = c_type
        self.supervisor_id = supervisor_id

