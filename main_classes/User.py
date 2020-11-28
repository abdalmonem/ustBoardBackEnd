import time
from enum import Enum
from random import uniform, randrange
from typing import List

from flask import Flask

from Util.ConnectionWorker import ConnectionWorker
from Util.Security import Security
from extensions import db
from sqlalchemy import exc, or_


from models.StudentModel import StudentModel
from models.SuperVisorModel import SuperVisorModel
from models.UserModel import UserModel

class UserRank(Enum):
    admin = 3
    supervisor = 2
    teacher = 1
    student = 0

class User(UserModel):
    _UserModel = None
    _StudentModel = None
    session = None

    def __init__(self):
        self.session = db.session

    def inject_model_data(self, row_data: List[any] = None):
        if row_data is not None:
            for item in row_data:
                try:
                    setattr(self, item, row_data[item])
                except:
                    None

    def set_rank(self, rank: UserRank):
        self.rank = rank.value

    def set_username(self, username: str):
        self.username = username

    def set_id(self, id: int):
        self.id = id

    def set_password(self, password: any):
        password = Security.encrypt_password(password=password)
        self.password = password

    def set_email(self, email: any):
        self.email = email

    def set_phone(self, phone: int):
        self.phone = phone

    def set_date(self, date: int):
        self.date = date


class Users:
    session = None
    year = None

    def __init__(self):
        self.session = db.session

    def set_year(self, year: int):
        if str(year).isnumeric():
            self.year = year

    @staticmethod
    def re_create_auth_key(self, user_id):
        new_auth_key = str(time.time()) + str(uniform(0, 10))
        new_auth_key = Security.encrypt_password(new_auth_key)
        self.session.query(User.id).filter(User.id == user_id).update({'auth_key': new_auth_key})
        self.session.commit()
        return new_auth_key

    @staticmethod
    def is_username_exist(self, username: str) -> bool:
        if self.session.query(User.username).filter(User.username == username).scalar() is not None:
            return True
        return False

    @staticmethod
    def is_email_exist(self, email: str) -> bool:
        if self.session.query(User.email).filter(User.email == email).scalar() is not None:
            return True
        return False

    def get(self, list_of_fields=None, list_of_filters=None) -> List[User]:
        list_of_users = []
        data = self.session.query(*list_of_fields).filter(*list_of_filters)

        for item in data.all():
            _item_instance = User()
            _item_instance.inject_model_data(row_data=item._asdict())
            list_of_users.append(_item_instance)

        return list_of_users

    def login(self, username: str = None, email: str = None, phone: str = None,
              password: str = None) -> ConnectionWorker:
        filter_factory = []
        if username is not None:
            filter_factory.append(User.username == username)
        elif email is not None:
            filter_factory.append(User.email == email)
        elif phone is not None:
            filter_factory.append(User.phone == phone)

        # لو المستخدم ما دخل لا يوزر لا إيميل لا تلفون
        if len(filter_factory) < 1:
            return ConnectionWorker().create_response(state=False, reason="there is no phone or email or username")

        # إذا المستخدم ما دخل كلمة المًرور
        if password is None or password == '':
            return ConnectionWorker().create_response(state=False, reason="password field is empty")

        # جلب بيانات المستخدم
        data = self.session.query(User.auth_key, User.id, User.password).filter(*filter_factory).first()
        if bool(data):
            data = data._asdict()
        else:
            return ConnectionWorker().create_response(state=False, reason="account not found")

        # كلمة المرور صحيحة
        if Security.encrypt_password(password=password) != data["password"]:
            return ConnectionWorker().create_response(state=False, reason="incorrect password")

        # توليد مفتاح توثيق جديد , ,تبديل المفتاح القديم
        data["auth_key"] = self.re_create_auth_key(self, data["id"])
        return ConnectionWorker().create_response(state=True, data={
            'auth_key': data["auth_key"],
            'id': data["id"],
        })

    # إنشاء عضو جديد
    def create(self, user: User = None) -> ConnectionWorker:
        state = True
        reason = ""
        _filters = []
        returned_data_body = None

        if user.password is None:
            user.set_password(str(time.time() + randrange(0, 10000)))

        if user is None:
            reason = "user is not passed"
            state = False

        if user.email is None and user.phone is None:
            reason = "email_and_phone_not_isset_should_select_one"
            state = False

        if user.email is not None:
            _filters.append(User.email == user.email)

        if user.username is not None:
            _filters.append(User.username == user.username)

        if user.phone is not None:
            _filters.append(User.phone == user.phone)

        data = self.session.query(User.phone, User.email, User.username).filter(or_(*_filters)).first()


        # في حال رقم التلفون أو البريد أو اسم المستخدم مستعمل
        if state and bool(data):
            state = False
            data = data._asdict()
            if data["phone"] == user.phone:
                reason = "phone number in use"
            if data["email"] == user.email:
                reason = "email in use"
            if data["username"] == user.username:
                reason = "username in use"

        if state:
            self.session.add(user)
            self.session.flush()

            if UserRank(user.rank) == UserRank.student:
                new_student = StudentModel()
                new_student.user_id = user.id
                new_student.department_id = None
                new_student.class_group_id = None
                new_student.lab_group_id = None
                new_student.year = self.year
                self.session.add(new_student)

            if UserRank(user.rank) == UserRank.supervisor:
                new_supervisor = SuperVisorModel()
                new_supervisor.user_id = user.id
                new_supervisor.department_id = None
                new_supervisor.year = self.year
                self.session.add(new_supervisor)

            returned_data_body = {}
            returned_data_body["id"] = user.id
            try:
                self.session.commit()
                state = True
            except exc.SQLAlchemyError as e:
                reason = "db_transaction_error"
                state = False

        return ConnectionWorker().create_response(reason=reason, state=state, data=returned_data_body)
