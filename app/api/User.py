from flask import request, current_app, url_for, redirect
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_raw_jwt,
    get_jwt_claims
)
from werkzeug.security import hashlib
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from .email import send_verfy_mail
from .decorators import supervisor_required, confirmed
from . import api, LogoutList
from .. import jwt, db
from ..models import Users, Teachers, Admin, Supervisor, Student
from ..schemas import UserSchema, TeacherSchema, AdminSchema, SupervisorSchema, StudentSchema
from itsdangerous import JSONWebSignatureSerializer as Serializer

user_schema = UserSchema()
admin_schema = AdminSchema()
super_schema = SupervisorSchema()
student_schema = StudentSchema()
teacher_schema = TeacherSchema()

@api.route('/')
def create_users():
    admin = Admin(
        username='stephy',
        email='stephy@outlook.com',
        password='990099',
        phone='0912533',
        surename='Areik Steven Donato',
        admin_card='AD03',
        gendre=0,
        confirmed=True
    )
    supervisor = Supervisor(
        username='nazaria',
        email='nazaria@hotmail.com',
        password='887788',
        phone='0999112',
        surename='Nazaria Esmail',
        super_card='SU02',
        gendre=0,
        confirmed=True
    )
    teacher = Teachers(
        username='osman',
        email='osman@gmail.com',
        password='5555',
        phone='012233',
        surename='Ali Esmail',
        teacher_card='TE02',
        gendre=0,
        confirmed=True
    )
    student = Student(
        username='malikah',
        email='malik@gmail.com',
        password='2020',
        phone='090001',
        surename='Malikah Kamal',
        card_id='IT2016B0525',
        gendre=1,
        confirmed=True,
        year='2016'
    )
    teacher.save_data()
    admin.save_data()
    supervisor.save_data()
    return {"msg": "data added"}

@api.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    try:
        data = user_schema.load(json_data)
    except ValidationError as error:
        raise error.messages
    user = Users.find_by_phone(data['phone'])
    if user and user.password_check(data['password']):
        if not user.confirmed:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_access_token(identity=user.id)
            confirm_code = user.generate_confirm_number(current_app.config['SECRET_KEY'], expiration=1800)
            serial = Serializer(current_app.config['SECRET_KEY'])
            try:
                data = serial.loads(confirm_code.encode('utf-8'))
            except:
                return {"msg": "couldn't load confirm"}
            if data['confirm_code']:
                send_verfy_again(user.email, current_app.config['UST_MAIL'], data['confirm_code'])
                return { 
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "id": user.id, "rank": user.rank,
                    "confirm code": confirm_code
                }, 200
        else:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_access_token(identity=user.id)
            return { 
                "access_token": access_token,
                "refresh_token": refresh_token,
                "id": user.id, "rank": user.rank
            }, 200
    else:
        return { "error": "Either User not found or Invalid \"input\"." }, 400

@api.route('/home', methods=['GET'])
@jwt_required
def home():
    confirm_code = request.headers['CONFIRM']
    if confirm_code:
        print(confirm_code)
        return {
            "msg": "check email for verfication number.",
            "url": url_for('/confirm')
        }
    return {"msg": "welcome home boddy!"}

@api.route('/profile/<string:username>', methods=['GET'])
@confirmed
def profile(username):
    try:
        user = Users.find_by_username(username)
    except IntegrityError as error:
        return error._message()
    if not user:
        return {"msg": "not found"}, 404
    userid = user.get_userid()
    user_rank = user.get_rank(userid)
    if user_rank == current_app.config['ADMIN_RANK']:
        user = Admin.find_by_username(username)
        admin_data = admin_schema.dump(user)
        return {"data:": admin_data}

    if user_rank == current_app.config['SUPERVISOR_RANK']:
        user = Supervisor.find_by_username(username)
        super_data = super_schema.dump(user)
        return {"data:": super_data}

    if user_rank == current_app.config['TEACHER_RANK']:
        user = Teachers.find_by_username(username)
        teacher_data = teacher_schema.dump(user)
        return {"data:": teacher_data}

    if user_rank == current_app.config['STUDENT_RANK']:
        user = Student.find_by_username(username)
        std_data = teacher_schema.dump(user)
        return {"data:": std_data}

@api.route('/profile/edit/<string:username>', methods=['PUT'])
@confirmed
def edit_profile(username):
    json_data = request.get_json()
    try:
        user = Users.find_by_username(username)
    except IntegrityError as error:
        return error._message()
    if not user:
        return {"msg": "not found"}, 404
    
    try:
        data = admin_schema.dump(user)
    except ValidationError as error:
        return error.messages, 400
    try:
        if 'email' in json_data:
            if Users.query.filter_by(email=json_data['email']).first():
                return {"msg": "email already exists"}, 500
            user.email = json_data['email']

        if 'phone' in json_data:
            if Users.find_by_phone(json_data['phone']):
                return {"msg": "phone already exists"}, 500
            user.phone = json_data['phone']

        if 'username' in json_data:
            if Users.find_by_username(json_data['username']):
                return {"msg": "username already token"}
            user.username = json_data['username']
        
        if 'surename' in json_data:
            user.surename = json_data['surename']
        if 'gendre' in json_data:
            user.gendre = json_data['gendre']
        if 'password' in json_data:
            user.set_passowrd(json_data['password'])
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    return {"data": admin_schema.dump(user)}

@api.route('/profile/delete/<string:username>', methods=['DELETE'])
@confirmed
@supervisor_required
def delete_user(username):
    try:
        user = Users.find_by_username(username=username)
    except IntegrityError as error:
        return error._message()
    if not user:
        return {"msg": "not fount"}
    try:
        user.delete_data()
    except IntegrityError as error:
        db.session.rollback()
        return error._message()

@api.route('/confirm/<string:username>', methods=['POST'])
@jwt_required
def confirm(username):
    confirm_code = request.headers['CONFIRM']
    json_data = request.get_json()
    user = Users.find_by_username(username)
    if json_data['confirm_code'] and confirm_code:
        serial = Serializer(current_app.config['SECRET_KEY'])
        try:
            loaded_data = serial.loads(confirm_code.encode('utf-8'))
        except:
            return {"msg": "couldn't load confirm"}
        if json_data['confirm_code'] == loaded_data['confirm_code']:
            user.confirmed = True
            db.session.commit()
            next = url_for('/change-password')
            if next:
                redirect(next)
            return {
                "msg": "Confirmation done, now change password.",
                "next_url": url_for('/home'),
            }
    return {"msg": "please make sure the confirmation number is correct."}, 400

@api.route('/edit-password/<int:id>', methods=['POST'])
@confirmed
def edit_password(id):
    json_data = request.get_json()
    user = Users.find_by_id(id)
    if user:
        hashed_old_password = hashlib.md5(json_data['old_password'].encode('utf-8')).hexdigest()
        hashed_new_password = hashlib.md5(json_data['new_password'].encode('utf-8')).hexdigest()
        if hashed_old_password == user.password:
            user.password = hashed_new_password
        else:
            return {"msg": "error, passwords isn't correct."}
    else:
        return {"msg": "usr not found"}, 404
    return {"msg": "Password updated correctly."}

@api.route('/logout', methods=['POST'])
@jwt_required
def logout():
    jwtID = get_raw_jwt()['jti']
    LogoutList.add(jwtID)
    return {"msg": "Logged out."}, 200
