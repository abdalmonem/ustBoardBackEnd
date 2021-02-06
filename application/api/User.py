from flask import request, current_app, url_for, redirect
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_raw_jwt,
    get_jwt_claims,
    verify_jwt_in_request
)
from werkzeug.security import hashlib
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from .email import send_verfy_mail
from .decorators import supervisor_required, confirmed
from . import api
from .. import jwt, db
from ..functions.LogoutList import LogoutList
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
        username='ste7en',
        email='ste7e@outlook.com',
        password='7777',
        phone='090144',
        surename='Areik Steven Donato',
        admin_card='AD2',
        gendre=0
    )
    supervisor = Supervisor(
        username='nazar',
        email='nazar@hotmail.com',
        password='9999',
        phone='9900',
        surename='Nazar Esmail',
        super_card='SU1',
        gendre=0
    )
    teacher = Teachers(
        username='ali',
        email='ali@gmail.com',
        password='1122',
        phone='1122',
        surename='Ali Esmail',
        teacher_card='TE1',
        gendre=0
    )
    student = Student(
        username='susan',
        email='susa@gmail.com',
        password='2020',
        phone='2020',
        surename='Susan Kamal',
        card_id='IT2016',
        gendre=0
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
                send_verfy_mail(user.email, current_app.config['UST_MAIL'], data['confirm_code'])
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
        return {"msg": "check email for verfication number."}
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
        user = Supervisor.find_by_username(username)
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
    if json_data['username'] == data['username'] or json_data['phone'] == data['phone']:
        return {"msg": "username or phone number already token"}, 400
    try:
        user.email = json_data['email']
        user.gendre = json_data['gendre']
        user.phone = json_data['phone']
        user.surename = json_data['surename']
        user.username = json_data['username']
        user.set_passowrd(data['password'])
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        return error._message(), 500
    return {"data": admin_schema.dump(user), "url": url_for('/profile/' + json_data['username'])}

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
            if next:
                redirect(next)
            return redirect(url_for('/home'))
    return {"msg": "please make sure the confirmation number is correct."}, 400

@api.route('/logout', methods=['POST'])
@jwt_required
def logout():
    jwtID = get_raw_jwt()['jti']
    LogoutList.add(jwtID)
    return {"msg": "Logged out."}, 200
