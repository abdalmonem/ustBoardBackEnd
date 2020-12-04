from configurations import db
from werkzeug.security import hashlib

class Users(db.Model):
    _tabelnsme_ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    surename = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Integer)
    rank = db.Column(db.Integer)

    def __init__(self, username, password, email, phone, surename, date):
        self.username = username
        self.password = hashlib.md5(password.encode('utf-8')).hexdigest()
        self.email = email
        self.phone = phone
        self.surename = surename
        self.date = date

    @classmethod
    def find_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_user_id(cls):
        return cls.id;

    def password_check(self, password):
        if self.password == hashlib.md5(password.encode('utf-8')).hexdigest():
            return True

    def save_data(self):
        db.session.add(self)
        db.session.commit()

