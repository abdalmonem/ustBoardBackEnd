from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from random import randint
from flask import current_app
from datetime import datetime
from werkzeug.security import hashlib
from .. import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    surename = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    rank = db.Column(db.Integer, default=0)
    gendre = db.Column(db.Boolean, nullable=True)
    confirmed = db.Column(db.Boolean, default=False)
    type = db.Column(db.String(50))

    def __init__(self, username, email, password, phone, surename, gendre):
        self.username = username
        self.email = email
        self.password = hashlib.md5(password.encode('utf-8')).hexdigest()
        self.phone = phone
        self.surename = surename
        self.gendre = gendre

    @classmethod
    def find_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def generate_confirm_number(self, secret_key, expiration=1800):
        serial = Serializer(secret_key, expiration)
        return serial.dumps({"confirm_code": randint(000000, 999999)}).decode('utf-8')

    def confirm(self):
        if self.confirmed == False:
            self.confirmed = True
            db.session.add(self)
            db.session.commit()
            return True

    def is_admin(self, rank):
        if rank == current_app.config['ADMIN_RANK']:
            return True
    
    def is_supervisor(self, rank):
        if rank == current_app.config['SUPERVISOR_RANK']:
            return True

    def is_teacher(self, rank):
        if rank == current_app.config['TEACHER_RANK']:
            return True

    def is_student(self, rank):
        if rank == current_app.config['STUDENT_RANK']:
            return True

    def password_check(self, password):
        if self.password == hashlib.md5(password.encode('utf-8')).hexdigest():
            return True

    def set_passowrd(self, password):
        self.password = hashlib.md5(password.encode('utf-8')).hexdigest()

    def get_rank(self, id):
        if id == self.id:
            return self.rank
        else:
            return False

    def username_exists(self, username):
        if username == self.username:
            return True
        else:
            return False

    def get_userid(self):
        return self.id

    def save_data(self):
        db.session.add(self)
        db.session.commit()

    def delete_data(self):
        db.session.delete(self)
        db.session.commit()
